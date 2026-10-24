#!/usr/bin/env python3
"""Caelvyr 1.1.0 premium flight-deck and scenery patch, applied after 1.0.1."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
html = root / "app/src/main/assets/index.html"
gradle = root / "app/build.gradle"
if not html.is_file() or not gradle.is_file():
    raise SystemExit("Android project not found: " + str(root))
s = html.read_text(encoding="utf-8")
original = s

# Remove the cluster-count feature left by the previous patch. Keep the expanded
# tree instance capacities and the independent, biome-aware distribution.
s = re.sub(r"  function cvForestStatsHTML\(\)\{.*?\n  \}\n", "", s, count=1, flags=re.S)
s = re.sub(
    r"\n    if \(menuTab === 'conditions'\) \{\s*el\.innerHTML = .*?cvForestStatsHTML\(\);\s*return;\s*\}",
    "",
    s,
    count=1,
    flags=re.S,
)
s = re.sub(r"\n\.mm-forest-stats\{[^\n]*\}\n\.mm-forest-total\{[^\n]*\}\n\.mm-forest-total b\{[^\n]*\}\n\.mm-forest-row\{[^\n]*\}\n\.mm-forest-row span\{[^\n]*\}", "", s)

# Keep the aircraft-preview camera where the player left it. Any scripted menu
# rotation is disabled; pointer drag below is the only source of camera motion.
if "window.__cvHangarCameraInitialized" not in s:
    s = re.sub(
        r"menuPreview\.el\s*=\s*0\.2;",
        "if (!window.__cvHangarCameraInitialized) { menuPreview.el = 0.2; window.__cvHangarCameraInitialized = true; }",
        s,
    )
s = re.sub(r"menuPreview\.theta\s*\+=\s*[^;]+;", "menuPreview.theta = menuPreview.theta;", s)
s = s.replace(
    "buildMenuHangar(ap, previewT, specs, clear);",
    "cvBuildPremiumHangar(ap, previewT, specs, clear);",
)

premium_css = r"""
/* CAELVYR 1.1.0 premium aeronautical flight-deck interface */
#menu-screen.mm{background:radial-gradient(ellipse at 52% 42%,#162a36 0%,#0a131b 48%,#05090e 100%)!important;color:#e9eef0!important;font-family:Inter,"Segoe UI",Roboto,system-ui,sans-serif!important}
#menu-screen .mm-top{display:flex!important;align-items:center!important;gap:20px!important;padding:18px clamp(14px,2.4vw,36px)!important;background:linear-gradient(180deg,#101d27f5,#0a141de8)!important;border-bottom:1px solid #c7a56a55!important;box-shadow:0 12px 34px #0005!important;backdrop-filter:blur(20px)!important}
#menu-screen .mm-title{font-size:clamp(15px,1.45vw,21px)!important;font-weight:850!important;letter-spacing:.24em!important;color:#f2f2e9!important;text-transform:uppercase!important}
#menu-screen .mm-sub{font-size:10px!important;letter-spacing:.20em!important;text-transform:uppercase!important;color:#9daeb7!important}
#menu-screen .mm-hint{color:#a4b2bb!important;font-size:10px!important;letter-spacing:.08em!important}
#menu-screen .mm-tabs{display:flex!important;gap:5px!important;padding:5px!important;background:#050c12c9!important;border:1px solid #71818c38!important;border-radius:7px!important}
#menu-screen .mm-tabs button{font-size:10px!important;letter-spacing:.13em!important;font-weight:800!important;color:#a9b6bd!important;border:1px solid transparent!important;border-radius:5px!important;background:transparent!important;transition:background .18s,border-color .18s,color .18s!important}
#menu-screen .mm-tabs button:hover{color:#f5e8c9!important;border-color:#bd9f6c55!important;background:#c4a36b12!important}
#menu-screen .mm-tabs button.active{background:linear-gradient(135deg,#d6c091,#b99b64)!important;color:#10161a!important;border-color:#edd7a0!important;box-shadow:0 4px 18px #c4a46b22!important}
#menu-screen .mm-main{display:flex!important;gap:clamp(12px,1.6vw,24px)!important;padding:clamp(12px,1.7vw,24px)!important;align-items:stretch!important}
#menu-screen .mm-panel{width:min(410px,34vw)!important;padding:clamp(15px,1.7vw,24px)!important;border:1px solid #a8b6bf25!important;border-top-color:#c2a36b6b!important;border-radius:8px!important;background:linear-gradient(145deg,#17232bf5,#0b141cf5 68%,#0a1117f5)!important;box-shadow:0 18px 55px #0007,inset 0 1px #ffffff08!important;backdrop-filter:blur(18px)!important}
#menu-screen .mm-panel h3,#menu-screen .mm-panel .mm-cat{color:#d2b77d!important;font:850 10px ui-monospace,SFMono-Regular,Consolas,monospace!important;letter-spacing:.18em!important;text-transform:uppercase!important}
#menu-screen .mm-panel h2{font-size:clamp(22px,2vw,32px)!important;line-height:1.08!important;letter-spacing:-.035em!important;font-weight:780!important;color:#f2f1e9!important}
#menu-screen .mm-desc{color:#aab7bd!important;font-size:12px!important;line-height:1.65!important}
#menu-screen .mm-item{position:relative!important;display:block!important;overflow:hidden!important;border:1px solid #9aabb522!important;border-radius:6px!important;background:linear-gradient(105deg,#202e37e8,#111c24f2)!important;padding:13px 14px!important;color:#e7eceb!important;box-shadow:inset 3px 0 transparent!important;transition:transform .16s,border-color .16s,background .16s!important}
#menu-screen .mm-item:hover{transform:translateX(2px)!important;border-color:#bca16d88!important;background:linear-gradient(105deg,#293a43,#13232c)!important}
#menu-screen .mm-item.sel{border-color:#d0b77f!important;background:linear-gradient(105deg,#5c5038a8,#1c2a31)!important;box-shadow:inset 3px 0 #ddc28a,0 0 0 1px #d7bc8130!important}
#menu-screen .mm-item .t{color:#f1f1e9!important;font-size:13px!important;font-weight:790!important;letter-spacing:.02em!important}
#menu-screen .mm-item .g,#menu-screen .mm-item .m{color:#97a9b2!important;font-size:10px!important;letter-spacing:.06em!important}
#menu-screen .mm-act{background:linear-gradient(135deg,#e1cc9d,#bb9f69)!important;color:#10161a!important;border:1px solid #f0d9a8!important;border-radius:5px!important;font-weight:850!important;letter-spacing:.11em!important}
#menu-screen .mm-bottom{background:linear-gradient(180deg,#0b141bdc,#060b10f7)!important;border-top:1px solid #bda16b40!important;padding:13px clamp(14px,2.4vw,36px) max(15px,env(safe-area-inset-bottom))!important}
#menu-screen .mm-start{background:linear-gradient(135deg,#ead5a4,#c0a26a)!important;color:#10161b!important;border:1px solid #f5e5bd!important;border-radius:5px!important;padding:15px 25px!important;font-size:12px!important;font-weight:950!important;letter-spacing:.17em!important;text-transform:uppercase!important;box-shadow:0 9px 28px #bd9c5c27!important}
#menu-screen .mm-start:hover{filter:brightness(1.08)!important;transform:translateY(-1px)!important}
#menu-screen input,#menu-screen select,#menu-screen textarea{background:#0b151c!important;border:1px solid #71818b70!important;border-radius:5px!important;color:#e8efed!important;accent-color:#d1b277!important}
#menu-screen input:focus,#menu-screen select:focus,#menu-screen textarea:focus{outline:1px solid #d2b579!important;border-color:#d2b579!important}
#menu-screen .mm-worldmap-card{background:#08131bbf!important;border-color:#b9a16d55!important;border-radius:6px!important}
.mm-world-map{background:#0b202b!important;border-color:#b9a16d66!important;border-radius:5px!important}
.mm-map-actions button{background:#17252d!important;border-color:#8799a54f!important;border-radius:4px!important;color:#e1e8e6!important;letter-spacing:.07em!important}
.mm-map-actions button:hover{background:#4b4536!important;border-color:#d2b477!important}
.mm-worldmap-selected{background:#c2a36b12!important;border-color:#c4a36b66!important;color:#e6d9b9!important;border-radius:4px!important}
#pause-screen{background:radial-gradient(ellipse at 50% 26%,#1a2a33f7,#05090dfd 74%)!important}
#pause-screen h1{color:#e4cf9e!important;letter-spacing:.24em!important;font-size:clamp(20px,3vw,32px)!important}
#pause-screen .menu-btn{background:linear-gradient(135deg,#e5d0a2,#bea06b)!important;color:#11171b!important;border-radius:5px!important;font-weight:850!important;letter-spacing:.11em!important}
#pause-screen .menu-btn.secondary{background:#17242ce8!important;color:#d9e0df!important;border:1px solid #9dabb64e!important}
@media(max-width:900px){#menu-screen .mm-top{gap:10px!important;padding:11px!important}#menu-screen .mm-tabs{width:100%!important;overflow-x:auto!important}#menu-screen .mm-tabs button{flex:0 0 auto!important;font-size:9px!important;letter-spacing:.06em!important}#menu-screen .mm-main{gap:10px!important;padding:8px!important}#menu-screen .mm-panel{width:auto!important;padding:13px!important}#menu-screen .mm-start{width:100%!important}#menu-screen .mm-bottom{gap:9px!important}#menu-screen .mm-map-actions{flex-wrap:wrap!important}#menu-screen .mm-map-actions button{min-width:44%!important}}
"""
if "/* CAELVYR 1.1.0 premium aeronautical flight-deck interface */" not in s:
    pos = s.rfind("</style>")
    if pos < 0:
        raise SystemExit("Cannot find style tag for 1.1.0 flight-deck CSS")
    s = s[:pos] + premium_css + "\n" + s[pos:]

# Procedural, offline-safe satellite-style textures and a terrain-only Ultra shader.
premium_js = r'''
/* CAELVYR 1.1.0 premium flight systems; procedural texture is satellite-style, not live imagery. */
var cvPremiumHangarGroup;
var cvSatelliteCanvas;
var cvAirportSatelliteMode = true;
var cvUltraShaderUniform = { value: 0 };
var cvTerrainMaterialCount = 0;

function cvSatelliteRandomFactory(seed) {
  var state = seed >>> 0;
  return function(){ state=(1664525*state+1013904223)>>>0; return state/4294967296; };
}
function cvCreateSatelliteCanvas() {
  var c=document.createElement('canvas'); c.width=1024; c.height=1024;
  var x=c.getContext('2d'), r=cvSatelliteRandomFactory(781203);
  var g=x.createLinearGradient(0,0,1024,1024);
  g.addColorStop(0,'#496447');g.addColorStop(.34,'#737452');g.addColorStop(.62,'#3c5d42');g.addColorStop(1,'#6f6849');
  x.fillStyle=g;x.fillRect(0,0,1024,1024);
  var fields=['#34573b','#45633e','#5f6842','#79734c','#8a7b57','#526346','#2f4f39','#77755a','#3e5947','#a18b63'];
  for(var i=0;i<1350;i++){
    var cx=r()*1024,cy=r()*1024,rx=4+r()*52,ry=3+r()*34,sides=5+Math.floor(r()*5),phase=r()*Math.PI*2;
    x.beginPath();
    for(var j=0;j<sides;j++){var a=phase+j*Math.PI*2/sides,rr=.68+r()*.55,px=cx+Math.cos(a)*rx*rr,py=cy+Math.sin(a)*ry*rr;if(j===0)x.moveTo(px,py);else x.lineTo(px,py);}
    x.closePath();x.fillStyle=fields[Math.floor(r()*fields.length)];x.globalAlpha=.14+r()*.26;x.fill();
  }
  x.globalAlpha=1;
  for(var k=0;k<42;k++){
    var sx=r()*1024,sy=r()*1024,ex=sx+(r()-.5)*420,ey=sy+(r()-.5)*420;
    x.beginPath();x.moveTo(sx,sy);x.quadraticCurveTo((sx+ex)/2+(r()-.5)*90,(sy+ey)/2+(r()-.5)*90,ex,ey);
    x.strokeStyle=k%4===0?'#c5b78b':'#c0ba9b';x.globalAlpha=k%4===0?.18:.08;x.lineWidth=k%4===0?2.4:1;x.stroke();
  }
  x.globalAlpha=1;
  for(var q=0;q<7;q++){
    var yy=90+q*143;x.beginPath();x.moveTo(-30,yy);x.bezierCurveTo(200,yy-65,280,yy+88,490,yy+10);x.bezierCurveTo(690,yy-80,800,yy+100,1050,yy-20);
    x.strokeStyle='#3d666e';x.lineWidth=11;x.globalAlpha=.36;x.stroke();x.strokeStyle='#6b8d85';x.lineWidth=3;x.globalAlpha=.22;x.stroke();
  }
  x.globalAlpha=1;
  var im=x.getImageData(0,0,1024,1024),d=im.data;
  for(var p=0;p<d.length;p+=4){var n=(r()-.5)*17;d[p]=Math.max(0,Math.min(255,d[p]+n));d[p+1]=Math.max(0,Math.min(255,d[p+1]+n));d[p+2]=Math.max(0,Math.min(255,d[p+2]+n*.72));}
  x.putImageData(im,0,0);return c;
}
function cvDisposeHangarGroup(group){
  if(!group)return;if(group.parent)group.parent.remove(group);
  group.traverse(function(o){
    if(o.geometry&&o.geometry.dispose)o.geometry.dispose();
    if(o.material){var ms=Array.isArray(o.material)?o.material:[o.material];ms.forEach(function(m){if(m&&m.userData&&m.userData.cvPremiumHangar){if(m.map&&m.map.dispose)m.map.dispose();if(m.dispose)m.dispose();}});}
  });
}
function cvBuildPremiumHangar(ap,t,specs,clear){
  try{
    if(typeof THREE==='undefined'||typeof scene==='undefined'||!scene||!t)return;
    if(cvPremiumHangarGroup)cvDisposeHangarGroup(cvPremiumHangarGroup);
    var group=new THREE.Group();group.name='Caelvyr_Premium_Hangar';
    var sc=Math.max(.65,Number(specs&&specs.scale)||1),st=planeStats(selectedPlaneKey);
    var span=Math.max(34,(st.span||38)*sc),length=Math.max(45,(st.length||45)*sc);
    var width=Math.max(130,Math.min(310,span*2.8)),depth=Math.max(170,Math.min(370,length*1.85+70)),height=Math.max(56,Math.min(112,span*.9+28));
    function mat(color,rough,metal,emissive,intensity){var m=new THREE.MeshStandardMaterial({color:color,roughness:rough,metalness:metal||0,emissive:emissive||0x000000,emissiveIntensity:intensity||0});m.userData.cvPremiumHangar=true;return m;}
    var floorMat=mat(0x343b3e,.92,.08),wallMat=mat(0x53616a,.82,.2),roofMat=mat(0x29353d,.72,.35),frameMat=mat(0x8d9798,.55,.68),darkMat=mat(0x171f24,.76,.32),yellowMat=mat(0xd4a943,.78,.12),whiteMat=mat(0xc5c8c1,.8,.05),lightMat=mat(0xe7eadc,.3,.08,0xe9e1c6,1.7);
    function box(w,h,d,px,py,pz,m){var o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(px,py,pz);group.add(o);return o;}
    var floor=new THREE.Mesh(new THREE.PlaneGeometry(width+24,depth+26),floorMat);floor.rotation.x=-Math.PI/2;floor.position.y=.05;group.add(floor);
    box(width,height,2,0,height/2,-depth/2,wallMat);
    box(2,height,depth,width/2,height/2,0,wallMat);box(2,height,depth,-width/2,height/2,0,wallMat);
    box(width+8,1.8,depth+8,0,height,0,roofMat);
    for(var ix of [-1,1])for(var iz of [-1,1])box(3.1,height+1.6,3.1,ix*(width/2-3),height/2,iz*(depth/2-3),frameMat);
    var baySpacing=Math.max(15,depth/7);
    for(var zz=-depth/2+12;zz<depth/2-6;zz+=baySpacing){
      box(width+1,1.4,1.8,0,height-2.8,zz,frameMat);
      box(1.5,4.5,1.5,-width*.28,height-6,zz,frameMat);box(1.5,4.5,1.5,width*.28,height-6,zz,frameMat);
    }
    box(width*.72,2.4,2.2,0,height-2.1,depth/2-3.5,frameMat);
    box(2.3,height-3,2.3,-width*.39,(height-3)/2,depth/2-3.5,frameMat);
    box(2.3,height-3,2.3,width*.39,(height-3)/2,depth/2-3.5,frameMat);
    box(width*.78,1.2,depth*.23,0,height-4,-depth*.34,darkMat);
    box(1.2,.08,depth-18,0,.16,0,yellowMat);box(.38,.07,depth-18,-width*.17,.15,0,whiteMat);box(.38,.07,depth-18,width*.17,.15,0,whiteMat);
    for(var zmark=-depth/2+16;zmark<depth/2-8;zmark+=12){box(5,.09,1.2,-width*.38,.17,zmark,yellowMat);box(5,.09,1.2,width*.38,.17,zmark,yellowMat);}
    for(var lx=-1;lx<=1;lx++){
      box(width*.22,.32,1.4,lx*width*.27,height-5,0,lightMat);
      var pl=new THREE.PointLight(0xffedce,.48,Math.min(width,depth)*.62,2);pl.position.set(lx*width*.27,height-8,0);group.add(pl);
    }
    var signCanvas=document.createElement('canvas');signCanvas.width=512;signCanvas.height=128;
    var sx=signCanvas.getContext('2d');sx.fillStyle='#101a20';sx.fillRect(0,0,512,128);sx.strokeStyle='#d0b77b';sx.lineWidth=5;sx.strokeRect(8,8,496,112);sx.fillStyle='#f0e6ce';sx.font='800 33px sans-serif';sx.textAlign='center';sx.fillText('CAELVYR',256,57);sx.fillStyle='#b8c4c7';sx.font='700 17px sans-serif';sx.fillText('AERONAUTICAL SERVICE HANGAR',256,87);
    var signTex=new THREE.CanvasTexture(signCanvas);if('colorSpace' in signTex&&THREE.SRGBColorSpace)signTex.colorSpace=THREE.SRGBColorSpace;
    var signMat=new THREE.MeshStandardMaterial({map:signTex,roughness:.68,metalness:.12,emissive:0x171717});signMat.userData.cvPremiumHangar=true;
    var sign=new THREE.Mesh(new THREE.PlaneGeometry(40,10),signMat);sign.position.set(0,height-10,-depth/2+1.2);group.add(sign);
    group.position.set(t.x,t.ground||0,t.z);if(t.quat&&group.quaternion)group.quaternion.copy(t.quat);
    scene.add(group);cvPremiumHangarGroup=group;
  }catch(err){console.warn('[Caelvyr hangar] premium hangar fallback:',err);}
}
function cvInstallUltraShader(material){
  if(!material||!material.onBeforeCompile||material.userData.cvUltraShaderInstalled)return;
  if(!(material.isMeshLambertMaterial||material.isMeshStandardMaterial||material.isMeshPhongMaterial))return;
  var oldCompile=material.onBeforeCompile,oldKey=material.customProgramCacheKey;
  material.onBeforeCompile=function(shader,rendererArg){
    oldCompile.call(this,shader,rendererArg);
    var common='#include <common>';
    if(shader.fragmentShader.indexOf(common)>=0)shader.fragmentShader=shader.fragmentShader.replace(common,common+'\nuniform float uCaelvyrUltraAmount;');
    var hook='#include <dithering_fragment>';
    if(shader.fragmentShader.indexOf(hook)>=0)shader.fragmentShader=shader.fragmentShader.replace(hook,hook+'\nfloat cvSlopeDetail=1.0-abs(normalize(normal).y);\nfloat cvMicrograin=sin(gl_FragCoord.x*.071+sin(gl_FragCoord.y*.043))*cos(gl_FragCoord.y*.061);\ngl_FragColor.rgb*=1.0+cvMicrograin*.009*uCaelvyrUltraAmount;\ngl_FragColor.rgb*=1.0-cvSlopeDetail*.035*uCaelvyrUltraAmount;\ngl_FragColor.rgb=(gl_FragColor.rgb-vec3(.5))*(1.0+.05*uCaelvyrUltraAmount)+vec3(.5);');
    shader.uniforms.uCaelvyrUltraAmount=cvUltraShaderUniform;
  };
  material.customProgramCacheKey=function(){return (oldKey?oldKey.call(this):'')+'|caelvyr-ultra-terrain-v1';};
  material.userData.cvUltraShaderInstalled=true;material.needsUpdate=true;
}
function cvUpgradeSceneryMaterials(){
  try{
    if(typeof THREE==='undefined'||typeof scene==='undefined'||!scene||!cvSatelliteCanvas)return;
    var texture=new THREE.CanvasTexture(cvSatelliteCanvas);texture.wrapS=texture.wrapT=THREE.RepeatWrapping;texture.repeat.set(7,7);texture.generateMipmaps=true;texture.minFilter=THREE.LinearMipmapLinearFilter;texture.magFilter=THREE.LinearFilter;
    if('colorSpace' in texture&&THREE.SRGBColorSpace)texture.colorSpace=THREE.SRGBColorSpace;
    if(typeof renderer!=='undefined'&&renderer&&renderer.capabilities&&renderer.capabilities.getMaxAnisotropy)texture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
    scene.traverse(function(o){
      if(!o.isMesh||o.isInstancedMesh||!o.geometry||!o.geometry.attributes||!o.geometry.attributes.uv)return;
      var name=String(o.name||'').toLowerCase();
      if(/water|ocean|sea|sky|cloud|runway|taxiway|airport|hangar|building|terminal|tree|forest|aircraft|plane/.test(name))return;
      var bounds=new THREE.Box3().setFromObject(o),size=bounds.getSize(new THREE.Vector3());
      var named=/terrain|island|landmass|worldground|groundsurface|continent/.test(name),large=size.x>500&&size.z>500&&size.y<Math.max(size.x,size.z)*.28;
      if(!named&&!large)return;
      var mats=Array.isArray(o.material)?o.material:[o.material];
      var changed=mats.map(function(m){
        if(!m||!m.color)return m;
        var hsl={h:0,s:0,l:0};m.color.getHSL(hsl);if(hsl.s>.25&&hsl.h>.48&&hsl.h<.77)return m;
        var clone=m.clone();clone.map=texture;if('roughness' in clone)clone.roughness=.96;if('metalness' in clone)clone.metalness=.02;clone.needsUpdate=true;cvInstallUltraShader(clone);cvTerrainMaterialCount++;return clone;
      });
      o.material=Array.isArray(o.material)?changed:changed[0];
    });
    texture.needsUpdate=true;
    console.info('[Caelvyr scenery] satellite-style terrain materials upgraded:',cvTerrainMaterialCount);
  }catch(err){console.warn('[Caelvyr scenery] texture upgrade skipped safely:',err);}
}
function cvSetUltraShaderEnabled(enabled){cvUltraShaderUniform.value=enabled?1:0;try{window.__CAELVYR_ULTRA_SHADER=!!enabled;}catch(_){}}
function cvInstallStationaryHangarCamera(){
  try{
    if(typeof renderer==='undefined'||!renderer||!renderer.domElement||typeof menuPreview==='undefined')return;
    var canvas=renderer.domElement,drag=null;canvas.style.cursor='grab';
    canvas.addEventListener('pointerdown',function(e){
      var menu=document.getElementById('menu-screen');if(!menu||menu.classList.contains('hidden')||e.button!==0)return;
      drag={x:e.clientX,y:e.clientY,theta:Number(menuPreview.theta)||0,el:Number(menuPreview.el)||.2};
      try{canvas.setPointerCapture(e.pointerId);}catch(_){}
      canvas.style.cursor='grabbing';
    });
    canvas.addEventListener('pointermove',function(e){if(!drag)return;menuPreview.theta=drag.theta-(e.clientX-drag.x)*.0085;menuPreview.el=Math.max(.025,Math.min(1.28,drag.el+(e.clientY-drag.y)*.006));});
    function stop(e){if(!drag)return;drag=null;canvas.style.cursor='grab';try{if(e&&canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);}catch(_){}}
    canvas.addEventListener('pointerup',stop);canvas.addEventListener('pointercancel',stop);canvas.addEventListener('lostpointercapture',stop);
    if(menuPreview.autoRotate!==undefined)menuPreview.autoRotate=false;
  }catch(err){console.warn('[Caelvyr camera] manual hangar pan unavailable:',err);}
}
(function cvBootPremiumFlightDeck(){
  cvSatelliteCanvas=cvCreateSatelliteCanvas();
  cvInstallStationaryHangarCamera();
  requestAnimationFrame(function(){cvUpgradeSceneryMaterials();});
  cvSetUltraShaderEnabled(false);
  document.addEventListener('click',function(e){
    var b=e.target&&e.target.closest?e.target.closest('button,[role="button"]'):null;if(!b)return;
    var label=String(b.innerText||b.textContent||'').trim().toUpperCase().replace(/\s+/g,' ');
    if(label==='ULTRA'||label==='ULTRA GRAPHICS'||label==='ULTRA QUALITY')cvSetUltraShaderEnabled(true);
    else if(label==='LOW'||label==='MEDIUM'||label==='HIGH'||label==='ULTRALOW'||label==='ULTRA LOW')cvSetUltraShaderEnabled(false);
  },true);
  document.addEventListener('change',function(e){var el=e.target;if(!el||el.tagName!=='SELECT')return;var v=String(el.value||'').trim().toLowerCase();if(v==='ultra')cvSetUltraShaderEnabled(true);else if(/^(ultralow|ultra-low|low|medium|high)$/.test(v))cvSetUltraShaderEnabled(false);},true);
})();
'''
if "/* CAELVYR 1.1.0 premium flight systems" not in s:
    pos = s.rfind("</script>")
    if pos < 0:
        raise SystemExit("Cannot find script tag for 1.1.0 flight systems")
    s = s[:pos] + premium_js + "\n" + s[pos:]

# Upgrade version markers and Android package version. Keep this patch repeatable.
s = s.replace("<!-- CAELVYR APP SHELL · V1.0.1 -->", "<!-- CAELVYR APP SHELL · V1.1.0 -->")
s = s.replace("const CV_APP_VERSION_FALLBACK = '1.0.1';", "const CV_APP_VERSION_FALLBACK = '1.1.0';")
g = gradle.read_text(encoding="utf-8")
g2 = re.sub(r"versionCode\s+\d+", "versionCode 3", g, count=1)
g2 = re.sub(r"versionName\s+'[^']+'", "versionName '1.1.0'", g2, count=1)
if "versionCode 3" not in g2 or "versionName '1.1.0'" not in g2:
    raise SystemExit("Could not update Android version to 1.1.0")
gradle.write_text(g2, encoding="utf-8")
if s != original:
    html.write_text(s, encoding="utf-8")
print("Caelvyr 1.1.0 premium flight-deck patch applied.")
print("Removed tree-cluster seeding and cluster statistics; kept higher-capacity independent tree pools.")
print("Added graphite/champagne UI, manual hangar camera, premium industrial hangar, procedural satellite-style scenery and Ultra terrain shader support.")
