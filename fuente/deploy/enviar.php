<?php
/**
 * Formulario de contacto · Plataforma Interprofesional Láctea, S.L.U.
 * Recibe la solicitud de solicitud.html (y sus versiones fr/pt/en) y la envía por correo.
 * Sin cookies, sin sesiones y sin servicios externos.
 */

// ---------------- Configuración ----------------
const DESTINO   = 'comercial@plataformalactea.com';   // quién recibe las solicitudes
const REMITENTE = 'comercial@plataformalactea.com';   // remitente (From) de los correos
const NOMBRE_REMITENTE = 'Web Plataforma Láctea';
const TIEMPO_MINIMO = 3;        // segundos mínimos entre abrir la página y enviar
const MAX_ENVIOS_POR_HORA = 5;  // por dirección IP
// ------------------------------------------------

header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

$ajax = isset($_SERVER['HTTP_X_REQUESTED_WITH']) && $_SERVER['HTTP_X_REQUESTED_WITH'] === 'fetch';

function responder(bool $ok, string $codigo, bool $ajax): void {
    if ($ajax) {
        http_response_code($ok ? 200 : ($codigo === 'metodo' ? 405 : 400));
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'error' => $ok ? null : $codigo]);
    } else {
        // Sin JavaScript: volvemos a la página del formulario con el resultado en la URL
        $volver = 'solicitud.html';
        $ref = $_SERVER['HTTP_REFERER'] ?? '';
        $host = $_SERVER['HTTP_HOST'] ?? '';
        $hostSinPuerto = preg_replace('/:\d+$/', '', $host);
        if ($ref !== '' && $host !== '' && parse_url($ref, PHP_URL_HOST) === $hostSinPuerto) {
            $volver = strtok($ref, '#');
        }
        header('Location: ' . $volver . ($ok ? '#enviado' : '#error'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    responder(false, 'metodo', $ajax);
}

// Campo trampa (honeypot): las personas no lo ven; los robots suelen rellenarlo.
// Se responde "ok" para no dar pistas al robot, pero no se envía nada.
if (!empty($_POST['web'] ?? '')) {
    responder(true, '', $ajax);
}

// Tiempo mínimo de relleno (el campo lo pone el navegador al cargar la página)
$t = (int)($_POST['t'] ?? 0);
$ahora = time();
if ($t <= 0 || ($ahora - $t) < TIEMPO_MINIMO || ($ahora - $t) > 172800) {
    responder(false, 'tiempo', $ajax);
}

// Límite de envíos por IP, guardado en un fichero temporal del servidor (sin cookies)
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$dirTmp = rtrim(sys_get_temp_dir(), '/');
$fichero = $dirTmp . '/pil_form_' . hash('sha256', $ip . __FILE__);
$marcas = [];
if (is_readable($fichero)) {
    $marcas = array_filter(array_map('intval', explode(',', (string)@file_get_contents($fichero))), function ($m) use ($ahora) {
        return $m > $ahora - 3600;
    });
}
if (count($marcas) >= MAX_ENVIOS_POR_HORA) {
    responder(false, 'limite', $ajax);
}

// Datos del formulario
function campo(string $n, int $max): string {
    $v = trim((string)($_POST[$n] ?? ''));
    $v = str_replace("\0", '', $v);
    return mb_substr($v, 0, $max, 'UTF-8');
}
function linea(string $v): string { // sin saltos de línea (evita inyección de cabeceras)
    return trim(preg_replace('/[\r\n\t]+/', ' ', $v));
}
$nombre   = linea(campo('nombre', 120));
$empresa  = linea(campo('empresa', 160));
$email    = linea(campo('email', 160));
$telefono = linea(campo('telefono', 40));
$pais     = linea(campo('pais', 80));
$tipo     = linea(campo('tipo', 80));
$producto = linea(campo('producto', 200));
$volumen  = linea(campo('volumen', 120));
$mensaje  = campo('mensaje', 5000);
$priv     = ($_POST['privacidad'] ?? '') === '1';
$idioma   = preg_replace('/[^a-z]/', '', strtolower(campo('idioma', 5))) ?: 'es';

if ($nombre === '' || $empresa === '' || $mensaje === '' || $pais === '' || $tipo === '' || !$priv
    || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    responder(false, 'datos', $ajax);
}
// Mensajes con muchos enlaces: casi siempre spam
if (preg_match_all('~https?://|www\.~i', $mensaje . ' ' . $producto) > 3) {
    responder(false, 'datos', $ajax);
}

// Correo
$asunto = 'Solicitud web: ' . $tipo . ' – ' . $empresa;
$cuerpo = "Nueva solicitud de contacto desde la web (" . strtoupper($idioma) . ")\n"
        . "------------------------------------------------\n"
        . "Nombre:      $nombre\n"
        . "Empresa:     $empresa\n"
        . "Email:       $email\n"
        . "Teléfono:    " . ($telefono !== '' ? $telefono : '-') . "\n"
        . "País:        $pais\n"
        . "Consulta:    $tipo\n"
        . "Producto:    " . ($producto !== '' ? $producto : '-') . "\n"
        . "Volumen:     " . ($volumen !== '' ? $volumen : '-') . "\n"
        . "------------------------------------------------\n"
        . "Mensaje:\n" . $mensaje . "\n"
        . "------------------------------------------------\n"
        . "Ha aceptado la política de privacidad. Enviado el " . date('d/m/Y H:i') . " desde la IP $ip.\n"
        . "Para contestar, use «Responder»: va directamente al cliente.\n";

$cab = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'From: ' . mb_encode_mimeheader(NOMBRE_REMITENTE, 'UTF-8', 'Q') . ' <' . REMITENTE . '>',
    'Reply-To: ' . mb_encode_mimeheader($nombre, 'UTF-8', 'Q') . ' <' . $email . '>',
    'X-Mailer: PHP',
];
$asuntoCod = mb_encode_mimeheader($asunto, 'UTF-8', 'Q');

// "-f" fija también el remitente técnico (Return-Path); algunos hostings no lo permiten
$ok = @mail(DESTINO, $asuntoCod, $cuerpo, implode("\r\n", $cab), '-f' . REMITENTE);
if (!$ok) {
    $ok = @mail(DESTINO, $asuntoCod, $cuerpo, implode("\r\n", $cab));
}
if (!$ok) {
    responder(false, 'envio', $ajax);
}

$marcas[] = $ahora;
@file_put_contents($fichero, implode(',', $marcas), LOCK_EX);
responder(true, '', $ajax);
