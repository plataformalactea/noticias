import fs from 'fs';
import {feature} from 'topojson-client';
import {geoNaturalEarth1, geoPath} from 'd3-geo';
const W=1000,H=520;
const land=JSON.parse(fs.readFileSync('node_modules/world-atlas/land-110m.json'));
const countries=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-110m.json'));
const L=feature(land,land.objects.land);
const C=feature(countries,countries.objects.countries);
const spain=C.features.find(f=>f.id==='724');
const proj=geoNaturalEarth1().fitExtent([[10,10],[W-10,H-10]],{type:'Sphere'});
proj.precision(0.3);
const path=geoPath(proj).digits(1);
const pts={madrid:[-3.7,40.4],
 paris:[2.35,48.85],london:[-0.1,51.5],amsterdam:[4.9,52.37],lisboa:[-9.14,38.72],milan:[9.19,45.46],berlin:[13.4,52.5],varsovia:[21.0,52.2],
 casablanca:[-7.6,33.6],argel:[3.06,36.75],dakar:[-17.4,14.7],lagos:[3.4,6.5],elcairo:[31.2,30.0],
 dubai:[55.3,25.2],riad:[46.7,24.7],mumbai:[72.8,19.1],singapur:[103.8,1.35],shanghai:[121.5,31.2],tokio:[139.7,35.7],
 nuevayork:[-74.0,40.7],miami:[-80.2,25.8],mexico:[-99.1,19.4],bogota:[-74.1,4.7],saopaulo:[-46.6,-23.5],buenosaires:[-58.4,-34.6],
 johannesburgo:[28.0,-26.2],sidney:[151.2,-33.9]};
const P={};for(const[k,v] of Object.entries(pts)) P[k]=proj(v).map(x=>+x.toFixed(1));
const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}"><path d="${path({type:'Sphere'})}" fill="#EAF1F8"/><path d="${path(L)}" fill="#C9D6E6" stroke="#FFFFFF" stroke-width="0.6"/><path d="${path(spain)}" fill="#3D5793"/></svg>`;
fs.writeFileSync('../prodimg/mapamundi.svg',svg);
fs.writeFileSync('points.json',JSON.stringify(P));
console.log(svg.length, JSON.stringify(P));
