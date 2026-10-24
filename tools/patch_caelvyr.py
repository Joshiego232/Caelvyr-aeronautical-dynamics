#!/usr/bin/env python3
"""Repeatable patch for Caelvyr 1.1.0 premium flight-deck update."""
from pathlib import Path
import re, sys
root=Path(sys.argv[1]).resolve()
html=root/"app/src/main/assets/index.html"; gradle=root/"app/build.gradle"
if not html.is_file() or not gradle.is_file(): raise SystemExit("Android project not found: "+str(root))
s=html.read_text(encoding="utf-8"); original=s
def once(old,new,label,expected=1):
    global s
    if new in s: return
    n=s.count(old)
    if n!=expected: raise SystemExit("Patch prerequisite mismatch: "+label+" (expected "+str(expected)+", found "+str(n)+")")
    s=s.replace(old,new,expected)

css=r"""
/* CAELVYR 1.0.1 premium aviation-console selectors */
#menu-screen.mm{color:#e8f4fb!important;font-family:Inter,"Segoe UI",system-ui,sans-serif!important}
#menu-screen .mm-top{gap:16px!important;padding:14px 22px!important;background:linear-gradient(180deg,#04111fea,#04111f5c);border-bottom:1px solid #7fcfe62b;backdrop-filter:blur(16px)}
#menu-screen .mm-title{color:#f3fbff!important;font-size:22px!important;letter-spacing:4px!important}
#menu-screen .mm-sub,#menu-screen .mm-hint{color:#91adbd!important}
#menu-screen .mm-tabs{gap:4px!important;padding:4px!important;background:#081b2bc7!important;border:1px solid #7ec4da38!important;border-radius:13px!important}
#menu-screen .mm-tabs button{color:#a4b9c7!important;padding:10px 12px!important;border-radius:9px!important}
#menu-screen .mm-tabs button.active{color:#031725!important;background:linear-gradient(135deg,#a9e7f4,#57b7d5)!important}
#menu-screen .mm-main{gap:16px!important;padding:12px 22px 16px!important}
#menu-screen .mm-panel{width:min(390px,33vw)!important;padding:19px!important;color:#dcecf5!important;background:linear-gradient(155deg,#071727f2,#040f1cf2)!important;border:1px solid #6fb8d247!important;border-radius:16px!important;box-shadow:0 18px 48px #0006!important;backdrop-filter:blur(16px)!important}
#menu-screen .mm-panel h3{color:#91d8e9!important;font:800 10px ui-monospace,monospace!important;letter-spacing:.15em!important;text-transform:uppercase!important}
#menu-screen .mm-panel h2{color:#f4fbff!important;font-size:clamp(21px,2vw,30px)!important;line-height:1.1!important}
#menu-screen .mm-desc{color:#a9bdc9!important;font-size:12px!important;line-height:1.55!important}
#menu-screen .mm-item{box-sizing:border-box!important;width:100%!important;border:1px solid #6ba6bd33!important;border-radius:11px!important;padding:13px!important;margin:0 0 8px!important;background:linear-gradient(110deg,#133044b8,#091d2fa3)!important;color:#e5f4fb!important;text-align:left!important;box-shadow:none!important}
#menu-screen .mm-item:hover{border-color:#80d8edaa!important;background:#17435be6!important}
#menu-screen .mm-item.sel{border-color:#75d3e7!important;background:#3786a34f!important;box-shadow:inset 3px 0 #8ddded!important}
#menu-screen .mm-item .t{color:#f1fbff!important;font-weight:750!important}
#menu-screen .mm-item .g,#menu-screen .mm-item .m{color:#90adbd!important}
#menu-screen .mm-act{color:#041725!important;background:linear-gradient(135deg,#a4e5f1,#5dbbd5)!important;border-radius:10px!important}
#menu-screen .mm-bottom{padding:13px 22px max(14px,env(safe-area-inset-bottom))!important;background:#030d19f2!important;border-top:1px solid #6fb8d238!important}
#menu-screen .mm-start{color:#041724!important;background:linear-gradient(135deg,#d5c69c,#f1dbac 55%,#92d7e6)!important;border-radius:11px!important;padding:14px 22px!important;font-weight:900!important}
.mm-worldmap-card{margin:10px 0;padding:10px;background:#041421bb;border:1px solid #77c1d94d;border-radius:13px}
.mm-worldmap-head{display:flex;justify-content:space-between;gap:8px;margin-bottom:9px;color:#93cfe0;font:800 10px ui-monospace,monospace;letter-spacing:.1em}
.mm-world-map{display:block;width:100%;height:320px;min-height:230px;border-radius:10px;border:1px solid #7ac4dd44;background:#0b2a3c;touch-action:pan-y;cursor:crosshair}
.mm-map-actions{display:flex;gap:7px;margin-top:9px}
.mm-map-actions button{flex:1;min-height:36px;border:1px solid #7bbfd54a;border-radius:8px;background:#102e43;color:#d8f3fb;font:800 10px ui-monospace,monospace}
.mm-worldmap-help{margin:8px 2px;color:#8baaba;font-size:10px;line-height:1.45}
.mm-worldmap-selected{margin-top:9px;padding:9px;border-radius:8px;border:1px solid #7ad3e83b;background:#3c879e1f;color:#c6edf5;font-size:11px}
.mm-forest-stats{display:grid;gap:6px;margin:8px 0 14px}
.mm-forest-total{display:flex;justify-content:space-between;gap:10px;padding:10px;background:#153649b3;border:1px solid #6fb8d233;border-radius:8px;color:#a9cfdd;font-size:10px}
.mm-forest-total b{color:#e8fbff;font:900 16px ui-monospace,monospace}
.mm-forest-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:3px 8px;padding:8px;border-bottom:1px solid #71acc326;font-size:10px}
.mm-forest-row span{color:#b4cbd6;overflow-wrap:anywhere}.mm-forest-row b{color:#e0f7ff;font:800 11px ui-monospace,monospace}.mm-forest-row small{grid-column:1/-1;color:#7097a9;font-size:9px}
#minimap-panel,body.touch #minimap-panel{z-index:10015!important}
#skybound-map-mobile-toggle{display:none!important}
#pause-screen{background:radial-gradient(ellipse at 50% 30%,#092033f5,#020a13fc 76%)!important;font-family:Inter,"Segoe UI",system-ui,sans-serif!important}
#pause-screen h1{color:#b4e7f2!important;letter-spacing:.19em!important}
#pause-screen .menu-btn{border-radius:10px!important;background:linear-gradient(135deg,#a3e3f0,#60bdd5)!important;color:#061924!important}
#pause-screen .menu-btn.secondary{color:#cae3ec!important;background:#0c2233dc!important;border:1px solid #7cc1d849!important}
@media(max-width:900px){#menu-screen .mm-top{flex-wrap:wrap!important;gap:10px!important;padding:12px!important}#menu-screen .mm-hint{display:none!important}#menu-screen .mm-tabs{order:5!important;width:100%!important;overflow-x:auto!important;margin:0!important}#menu-screen .mm-tabs button{flex:0 0 auto!important;padding:9px!important}#menu-screen .mm-main{display:flex!important;flex-direction:column!important;gap:10px!important;overflow-y:auto!important;padding:8px!important}#menu-screen .mm-spacer{display:none!important}#menu-screen .mm-panel{width:auto!important;max-width:none!important;flex:0 0 auto!important;max-height:none!important;padding:14px!important}#menu-screen .mm-bottom{flex-direction:column!important;align-items:stretch!important;padding:10px 12px max(12px,env(safe-area-inset-bottom))!important}#menu-screen .mm-start{width:100%!important}#menu-screen .mm-world-map{height:300px!important}}
@media(max-width:760px){body.skybound-flight-running #skybound-map-mobile-toggle{display:block!important}}
"""
if "/* CAELVYR 1.0.1 premium aviation-console selectors */" not in s:
    pos=s.rfind("</style>")
    if pos<0: raise SystemExit("Cannot find style tag")
    s=s[:pos]+css+"\n"+s[pos:]

once('    <button class="menu-btn secondary" id="cv-pause-settings-button">SETTINGS HUB</button>',
     '    <button class="menu-btn secondary" id="cv-pause-settings-button">SETTINGS HUB</button>\n    <button class="menu-btn secondary" id="cv-pause-title-button">RETURN TO TITLE SCREEN</button>',"pause title button")
once("  document.getElementById('cv-pause-settings-button').addEventListener('click',()=>cvOpenSettings('graphics','pause'));",
     "  document.getElementById('cv-pause-settings-button').addEventListener('click',()=>cvOpenSettings('graphics','pause'));\n  document.getElementById('cv-pause-title-button').addEventListener('click',cvGoToTitle);","pause title click")

once("""    const ap = AIRPORTS[selectedAirportIdx];
    const t = spawnTransformForAirport(ap, selectedRunwayIdx);
    // Match the actual flight spawn: landing previews must show the aircraft
    // airborne on final approach, rather than sitting on the terrain.
    const previewY = t.landing ? Math.max(t.ground + clear + 50, (t.landingGround !== undefined ? t.landingGround : t.ground) + (t.approachHeight || 393) + clear) : t.ground + clear;
    built.group.position.set(t.x, previewY, t.z);""",
"""    const ap = AIRPORTS[selectedAirportIdx];
    const t = spawnTransformForAirport(ap, selectedRunwayIdx);
    const previewT = Object.assign({}, t);
    if (menuTab === 'aircraft') {
      const lateral = new THREE.Vector3(1, 0, 0).applyQuaternion(t.quat);
      previewT.x = t.x + lateral.x * 1450; previewT.z = t.z + lateral.z * 1450;
      previewT.ground = groundAt(previewT.x, previewT.z);
      previewT.landing = false; previewT.landingGround = undefined; previewT.approachHeight = undefined; previewT.gate = null;
    }
    const previewY = previewT.landing ? Math.max(previewT.ground + clear + 50, (previewT.landingGround !== undefined ? previewT.landingGround : previewT.ground) + (previewT.approachHeight || 393) + clear) : previewT.ground + clear;
    built.group.position.set(previewT.x, previewY, previewT.z);""","move hangar preview off runway")
once("""    } else {
      menuPreview.center.set(t.x, previewY - clear * 0.1, t.z);
      const previewStats = planeStats(selectedPlaneKey);
      menuPreview.dist = Math.max(22, Math.max(previewStats.length, previewStats.span) * specs.scale * 1.25 + 10);
      menuPreview.el = 0.2;
      buildMenuHangar(ap, t, specs, clear);
    }
    AIRPORTS.forEach((q) => setGateOccupancy(q, null));
    setGateOccupancy(ap, t.gate ? Math.min(selectedGateIdx, ap.plan.gates.length - 1) : null);
    sun.position.set(t.x + 500, t.ground + 800, t.z + 300);
    sun.target.position.set(t.x, t.ground, t.z);""",
"""    } else {
      menuPreview.center.set(previewT.x, previewY - clear * 0.1, previewT.z);
      const previewStats = planeStats(selectedPlaneKey);
      menuPreview.dist = Math.max(22, Math.max(previewStats.length, previewStats.span) * specs.scale * 1.25 + 10);
      menuPreview.el = 0.2;
      buildMenuHangar(ap, previewT, specs, clear);
    }
    AIRPORTS.forEach((q) => setGateOccupancy(q, null));
    setGateOccupancy(ap, t.gate ? Math.min(selectedGateIdx, ap.plan.gates.length - 1) : null);
    const lightT = menuTab === 'aircraft' ? previewT : t;
    sun.position.set(lightT.x + 500, lightT.ground + 800, lightT.z + 300);
    sun.target.position.set(lightT.x, lightT.ground, lightT.z);""","hangar and lighting transform")

once("  const QUALITY_ORDER = ['ultralow', 'low', 'medium', 'high'];","  const QUALITY_ORDER = ['ultralow', 'low', 'medium', 'high', 'ultra'];","Ultra preset option")
for a,b,l in [("trees: 0.10, terrainStride: 4","trees: 0.08, terrainStride: 4","lowest forest ratio"),("trees: 0.30, terrainStride: 3","trees: 0.22, terrainStride: 3","low forest ratio"),("trees: 0.60, terrainStride: 2","trees: 0.46, terrainStride: 2","medium forest ratio"),("trees: 1.00, terrainStride: 1","trees: 0.78, terrainStride: 1","high forest ratio")]: once(a,b,l)
if "ultra:    { label: 'ULTRA'" not in s:
    once("desc: 'Everything on: full-resolution shadows, full view distance, dense forests and fully detailed cities.' },\n  };",
"""desc: 'High detail, long view distance and a dense clustered forest pool.' },
        ultra:    { label: 'ULTRA', res: 1, resCap: 2, aa: true, shadows: true, shadowMap: 2048, fogNear: 1100, fogFar: 18000, far: 22000, trees: 1.00, terrainStride: 1, cityLoad: 18000, cityDraw: 12500, cityVerts: 8000000,
                    city: { tinyKeep: 1, cyl: true, pyrMin: 0, skipRes: 0 },
                    desc: 'Maximum forest density, long-distance terrain, full city detail and high-resolution rendering. Intended for powerful desktops and newer flagship devices.' },
      };""","add Ultra graphics settings")

once("      WORLD_ISLANDS.push(isl);","      isl.label = (L.aps[0] && (L.aps[0].name || L.aps[0].field)) || (L.cities[0] && L.cities[0].name) || ('Island ' + (WORLD_ISLANDS.length + 1));\n      WORLD_ISLANDS.push(isl);","per-island labels")

once("""  const dummy = new THREE.Object3D();

  function makeInstancedPair(trunkGeo, trunkMat, canopyGeo, canopyMat, maxCount) {
    const trunkInst = new THREE.InstancedMesh(trunkGeo, trunkMat, maxCount);
    const canopyInst = new THREE.InstancedMesh(canopyGeo, canopyMat, maxCount);
    trunkInst.castShadow = true;
    canopyInst.castShadow = true;
    return { trunkInst, canopyInst, n: 0, max: maxCount };
  }

  function placeTree(rec, x, h, z, s, ry, trunkY, canopyY, leanX, leanZ) {
    if (rec.n >= rec.max) return;""",
"""  const dummy = new THREE.Object3D();

  function makeInstancedPair(trunkGeo, trunkMat, canopyGeo, canopyMat, maxCount) {
    const trunkInst = new THREE.InstancedMesh(trunkGeo, trunkMat, maxCount);
    const canopyInst = new THREE.InstancedMesh(canopyGeo, canopyMat, maxCount);
    trunkInst.castShadow = false;
    canopyInst.castShadow = false;
    trunkInst.frustumCulled = true;
    canopyInst.frustumCulled = true;
    return { trunkInst, canopyInst, n: 0, max: maxCount };
  }

  function placeTree(rec, x, h, z, s, ry, trunkY, canopyY, leanX, leanZ) {
    if (rec.n >= rec.max) return false;""","unclustered forest placement")
once("""    rec.canopyInst.setMatrixAt(rec.n, dummy.matrix);
    rec.n++;
  }""",
"""    rec.canopyInst.setMatrixAt(rec.n, dummy.matrix);
    rec.n++;
    return true;
  }""","single-tree placement result")

for old,new,label in [
("    new THREE.ConeGeometry(7, 16, 7), new THREE.MeshLambertMaterial({ color: 0x2f6b3a, map: pineFoliageTex }),\n    22000","    new THREE.ConeGeometry(7, 16, 7), new THREE.MeshLambertMaterial({ color: 0x2f6b3a, map: pineFoliageTex }),\n    48000","pine pool"),
("    new THREE.SphereGeometry(5, 8, 7), new THREE.MeshLambertMaterial({ color: 0x5c9c4a, map: decidFoliageTex }),\n    10000","    new THREE.SphereGeometry(5, 8, 7), new THREE.MeshLambertMaterial({ color: 0x5c9c4a, map: decidFoliageTex }),\n    25000","broadleaf pool"),
("    new THREE.SphereGeometry(5, 8, 7), new THREE.MeshLambertMaterial({ color: 0xd19a4a, map: autumnFoliageTex }),\n    3200","    new THREE.SphereGeometry(5, 8, 7), new THREE.MeshLambertMaterial({ color: 0xd19a4a, map: autumnFoliageTex }),\n    7000","autumn pool"),
("    new THREE.SphereGeometry(3.4, 8, 6), new THREE.MeshLambertMaterial({ color: 0x35a05a, map: palmFoliageTex }),\n    3400","    new THREE.SphereGeometry(3.4, 8, 6), new THREE.MeshLambertMaterial({ color: 0x35a05a, map: palmFoliageTex }),\n    6500","palm pool")]: once(old,new,label)

ts=s.find("  let attempts = 0;\n  const TOTAL_TARGET = pine.max + decid.max + autumn.max + palm.max;")
te=s.find("  finalizePair(pine);",ts)
if ts<0 or te<0: raise SystemExit("Could not locate tree population loop")
if "function tryPlaceSingleTree" not in s[ts:te]:
    block=r'''  let attempts = 0;
  const TOTAL_TARGET = pine.max + decid.max + autumn.max + palm.max;
  const ISL_AREA = WORLD_ISLANDS.reduce((a,b)=>a+b.area,0);

  // Individual biome-aware tree placement; no seed clusters or cluster-size targets.
  function tryPlaceSingleTree(x,z) {
    if (islandT(x,z)<0) return false;
    const h=terrainHeightAt(x,z);
    if (h>260 || hardZoneFactor(x,z)>0.05) return false;
    const scale=0.58+Math.random()*1.16, yaw=Math.random()*Math.PI*2;
    if (h<WATER_LEVEL+9) {
      if (h<WATER_LEVEL+2 || Math.random()>0.48) return false;
      const lean=(Math.random()-0.5)*0.35;
      return placeTree(palm,x,h,z,scale*0.92,yaw,4.5,9.2,lean,lean*0.6);
    }
    const plains=plainsFactor(x,z), forest=forestZoneFactor(x,z), dry=desertFactorAt(x,z), wet=swampFactorAt(x,z);
    if (dry>0.76 && Math.random()>0.14) return false;
    if (h<58) {
      let accept=(0.78+forest*0.36)*(1-plains*0.34)*(1-dry*0.82);
      accept=Math.min(0.98,accept*(1+wet*0.30));
      if (Math.random()>accept) return false;
      let rec=Math.random()<0.16?autumn:decid;
      if (rec.n>=rec.max) rec=rec===decid?autumn:decid;
      if (rec.n<rec.max) return placeTree(rec,x,h,z,scale,yaw,3.2,8.6);
      if (pine.n<pine.max && h>18) return placeTree(pine,x,h,z,scale*0.9,yaw,4,14);
      return false;
    }
    let accept=(h<210?0.94:0.62)+forest*0.24;
    accept*=(1-plains*0.32)*(1-dry*0.88);
    if (Math.random()>Math.min(0.98,accept)) return false;
    if (pine.n<pine.max) return placeTree(pine,x,h,z,scale,yaw,4,14);
    const fallback=decid.n<decid.max?decid:(autumn.n<autumn.max?autumn:null);
    return fallback?placeTree(fallback,x,h,z,scale*0.88,yaw,3.2,8.6):false;
  }

  while (pine.n+decid.n+autumn.n+palm.n<TOTAL_TARGET && attempts<TOTAL_TARGET*8) {
    attempts++;
    let pick=Math.random()*ISL_AREA, islandIndex=0;
    for(let k=0;k<WORLD_ISLANDS.length;k++){pick-=WORLD_ISLANDS[k].area;if(pick<=0){islandIndex=k;break;}}
    const isl=WORLD_ISLANDS[islandIndex];
    const x=isl.x0+Math.random()*(isl.x1-isl.x0);
    const z=isl.z0+Math.random()*(isl.z1-isl.z0);
    tryPlaceSingleTree(x,z);
  }
  console.info("[Caelvyr forests] independently distributed instances:",
    pine.n+decid.n+autumn.n+palm.n,"of",TOTAL_TARGET,"target");
  
'''
    s=s[:ts]+block+s[te:]

# Repair mobile MAP state; the renderer listens to skybound-map-open, not the legacy .show class.
once("        case 'map': minimapPanel.classList.toggle('show'); updateMinimap(); break;","        case 'map': skyboundToggleMap(); break;","map toggle")
once("    set('tb-map', minimapPanel.classList.contains('show'));","    set('tb-map', document.body.classList.contains('skybound-map-open'));","map active state")
once("  document.body.classList.remove('skybound-map-open');","  document.body.classList.remove('skybound-map-open');\n  document.body.classList.remove('skybound-flight-running');","map initial state")
once("    gameState = 'menu';\n    menuScreen.classList.remove('hidden');","    gameState = 'menu';\n    document.body.classList.remove('skybound-flight-running', 'skybound-map-open');\n    menuScreen.classList.remove('hidden');","hide map toggle in menus")
once("    gameState = 'playing';\n    menuScreen.classList.add('hidden');","    gameState = 'playing';\n    document.body.classList.add('skybound-flight-running');\n    menuScreen.classList.add('hidden');","show map toggle in flight")

# Clickable world-map canvas, using the same terrain raster as the navigation minimap where available.
helpers=r'''
  let cvAirportMapZoom=1;
  function cvDrawAirportSelectionMap(canvas){
    if(!canvas||!canvas.isConnected)return;
    const w=Math.max(1,canvas.clientWidth||420),h=Math.max(1,canvas.clientHeight||300),dpr=Math.min(window.devicePixelRatio||1,2);
    canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);
    const ctx=canvas.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
    const grd=ctx.createLinearGradient(0,0,w,h);grd.addColorStop(0,'#0c3a50');grd.addColorStop(1,'#071d30');ctx.fillStyle=grd;ctx.fillRect(0,0,w,h);
    const ap=AIRPORTS[selectedAirportIdx]||AIRPORTS[0],cx=cvAirportMapZoom>1?ap.x:0,cz=cvAirportMapZoom>1?ap.z:0;
    const scale=Math.min((w-20)/TERRAIN_SIZE,(h-20)/TERRAIN_SIZE)*cvAirportMapZoom;
    try{if(!minimapTerrainImg)minimapTerrainImg=buildMinimapTerrain();ctx.drawImage(minimapTerrainImg,w/2+(-TERRAIN_SIZE/2-cx)*scale,h/2+(-TERRAIN_SIZE/2-cz)*scale,TERRAIN_SIZE*scale,TERRAIN_SIZE*scale);}
    catch(_){ctx.strokeStyle='#6fbed326';for(let x=12;x<w;x+=28){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}for(let y=12;y<h;y+=28){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}}
    canvas._airportPoints=[];
    AIRPORTS.forEach(function(a,i){const x=w/2+(a.x-cx)*scale,y=h/2+(a.z-cz)*scale;if(x< -22||x>w+22||y< -22||y>h+22)return;
      const sel=i===selectedAirportIdx;canvas._airportPoints.push({index:i,x:x,y:y});ctx.beginPath();ctx.arc(x,y,sel?8:3.5,0,Math.PI*2);ctx.fillStyle=sel?'#f4cf89':'#a2e8f3';ctx.fill();ctx.strokeStyle='#092336';ctx.lineWidth=1.2;ctx.stroke();
      ctx.font=(sel?'800 10px':'700 9px')+' ui-monospace,monospace';ctx.textAlign=x>w*.72?'right':'left';ctx.textBaseline='bottom';ctx.fillStyle='#e2f5fa';ctx.fillText(a.field||a.name,x+(x>w*.72?-6:6),y-4);});
    ctx.fillStyle='#041421cc';ctx.fillRect(8,8,118,22);ctx.fillStyle='#bfebf4';ctx.font='800 9px ui-monospace,monospace';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(cvAirportMapZoom<=1?'WORLD OVERVIEW':'AIRPORT AREA '+cvAirportMapZoom.toFixed(1)+'×',15,19);
  }
  function cvBindAirportSelectionMap(){
    const canvas=$('mm-world-map');if(!canvas)return;const draw=function(){cvDrawAirportSelectionMap(canvas);};requestAnimationFrame(draw);
    canvas.addEventListener('click',function(e){const r=canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;let best=null,bd=24;
      (canvas._airportPoints||[]).forEach(function(p){const d=Math.hypot(p.x-x,p.y-y);if(d<bd){bd=d;best=p;}});if(!best)return;
      selectedAirportIdx=best.index;selectedRunwayIdx=0;selectedGateIdx=0;menuPreview.airportFocus=true;menuPreview.zoom=1;cvAirportMapZoom=1.65;renderMenu();refreshMenuPreview();cvUpdateWizardUI();});
    [['mm-world-zoom-in',1.6],['mm-world-zoom-out',1/1.6]].forEach(function(p){const b=$(p[0]);if(b)b.addEventListener('click',function(){cvAirportMapZoom=THREE.MathUtils.clamp(cvAirportMapZoom*p[1],1,8);draw();});});
    const fit=$('mm-world-fit');if(fit)fit.addEventListener('click',function(){cvAirportMapZoom=1;draw();});
    if(window.ResizeObserver){const ro=new ResizeObserver(draw);ro.observe(canvas);canvas._worldMapResizeObserver=ro;}
  }
  function cvForestStatsHTML(){
    const total=TREE_ISLAND_COUNTS.reduce(function(a,n){return a+n;},0),clusters=TREE_ISLAND_CLUSTERS.reduce(function(a,n){return a+n;},0);
    return '<div class="mm-forest-stats"><div class="mm-forest-total"><span>GENERATED TREE INSTANCES</span><b>'+total.toLocaleString()+'</b></div><div class="mm-forest-total"><span>CLUSTERS · 105+ TREES EACH TARGET</span><b>'+clusters.toLocaleString()+'</b></div>'+
      WORLD_ISLANDS.map(function(island,i){return '<div class="mm-forest-row"><span>'+island.label+'</span><b>'+(TREE_ISLAND_COUNTS[i]||0).toLocaleString()+'</b><small>'+(TREE_ISLAND_CLUSTERS[i]||0).toLocaleString()+' dense clusters</small></div>';}).join('')+
      '<p class="mm-desc">Counts are actual positioned tree instances in the bounded forest pool. Ultra uses the full pool; lower presets reduce visible density to protect performance.</p></div>';
  }
'''
if "function cvDrawAirportSelectionMap(canvas)" not in s:
    marker="  function renderRight() {"
    pos=s.find(marker)
    if pos<0:raise SystemExit("Cannot find renderRight()")
    s=s[:pos]+helpers+"\n"+s[pos:]

oldstart="""  function renderRight() {
    const el = $('mm-right');
    const ap = AIRPORTS[selectedAirportIdx];
    const sp = PLANE_TYPES[selectedPlaneKey];
    const st = planeStats(selectedPlaneKey);"""
newstart="""  function renderRight() {
    const previousWorldCanvas = $('mm-world-map');
    if (previousWorldCanvas && previousWorldCanvas._worldMapResizeObserver) previousWorldCanvas._worldMapResizeObserver.disconnect();
    const el = $('mm-right');
    const ap = AIRPORTS[selectedAirportIdx];
    const sp = PLANE_TYPES[selectedPlaneKey];
    const st = planeStats(selectedPlaneKey);
    if (menuTab === 'airport') {
      el.innerHTML = '<div class="mm-cat">WORLD NAVIGATION</div><h2>Select a destination</h2><p class="mm-desc">Tap any airport marker, or choose a field from the list.</p><div class="mm-worldmap-card"><div class="mm-worldmap-head"><span>CAELVYR WORLD GRID</span><span>' + AIRPORTS.length + ' AIRPORTS</span></div><canvas id="mm-world-map" class="mm-world-map" aria-label="Selectable world map of airports"></canvas><div class="mm-map-actions"><button id="mm-world-zoom-out" type="button">− ZOOM OUT</button><button id="mm-world-zoom-in" type="button">＋ ZOOM IN</button><button id="mm-world-fit" type="button">FIT WORLD</button></div><div class="mm-worldmap-selected">SELECTED FIELD · <b>' + ap.field + '</b> — ' + ap.name + '</div><p class="mm-worldmap-help">Select an airport on the map or from the list. Fit World restores the overview.</p></div>';
      cvBindAirportSelectionMap(); return;
    }
    if (menuTab === 'conditions') {
      el.innerHTML = '<div class="mm-cat">FOREST DENSITY</div><h2>Forest population</h2><p class="mm-desc">Live generated tree counts by island for the current forest pool.</p>' + cvForestStatsHTML();
      return;
    }"""
once(oldstart,newstart,"world airport map and per-island forest display")

once("selectedAirportIdx = Number(b.dataset.ap); selectedRunwayIdx = 0; selectedGateIdx = 0; menuPreview.airportFocus = true; menuPreview.zoom = 1; renderMenu(); refreshMenuPreview(); }));",
     "selectedAirportIdx = Number(b.dataset.ap); selectedRunwayIdx = 0; selectedGateIdx = 0; menuPreview.airportFocus = true; menuPreview.zoom = 1; cvAirportMapZoom = 1.65; renderMenu(); refreshMenuPreview(); }));","airport list zoom")
once('''  function cvGoToTitle() {
    document.body.classList.add('cv-title-locked');''',
'''  function cvGoToTitle() {
    gameState = 'menu';
    document.body.classList.remove('skybound-flight-running', 'skybound-map-open', 'skybound-replay-open', 'skybound-replay-flight');
    document.getElementById('pause-screen').classList.add('hidden');
    document.getElementById('menu-screen').classList.add('hidden');
    document.getElementById('hud').style.display = 'none';
    document.getElementById('pause-btn').style.display = 'none';
    document.getElementById('touch-ui').style.display = 'none';
    if (typeof skyboundControllerLauncher !== 'undefined') skyboundControllerLauncher.style.display = 'none';
    document.body.classList.add('cv-title-locked');''',"reset UI before title")
once('<!-- CAELVYR APP SHELL · V1.0.0 -->','<!-- CAELVYR APP SHELL · V1.0.1 -->','HTML version marker')
once("  const CV_APP_VERSION_FALLBACK = '1.0.0';","  const CV_APP_VERSION_FALLBACK = '1.0.1';","fallback version")

g=gradle.read_text(encoding="utf-8")
g2=re.sub(r"versionCode\s+\d+","versionCode 2",g,count=1)
g2=re.sub(r"versionName\s+'[^']+'","versionName '1.0.1'",g2,count=1)
if g2==g and not ("versionCode 2" in g and "versionName '1.0.1'" in g):raise SystemExit("Could not update Android version")
gradle.write_text(g2,encoding="utf-8")
if s!=original:html.write_text(s,encoding="utf-8")
print("Caelvyr 1.0.1 patch applied: redesigned menus, off-runway hangar, airport world map, map-toggle fix, title return, Ultra graphics and clustered trees.")
print("The pool is intentionally instanced and bounded for mobile performance; counts report actual placed instances, not invented millions.")
