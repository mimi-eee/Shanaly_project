if(!self.define){let e,i={};const s=(s,n)=>(s=new URL(s+".js",n).href,i[s]||new Promise((i=>{if("document"in self){const e=document.createElement("script");e.src=s,e.onload=i,document.head.appendChild(e)}else e=s,importScripts(s),i()})).then((()=>{let e=i[s];if(!e)throw new Error(`Module ${s} didn’t register its module`);return e})));self.define=(n,r)=>{const l=e||("document"in self?document.currentScript.src:"")||location.href;if(i[l])return;let o={};const t=e=>s(e,l),a={module:{uri:l},exports:o,require:t};i[l]=Promise.all(n.map((e=>a[e]||t(e)))).then((e=>(r(...e),o)))}}define(["./workbox-3e911b1d"],(function(e){"use strict";self.skipWaiting(),e.clientsClaim(),e.precacheAndRoute([{url:"assets/index-Bub3Nrng.css",revision:null},{url:"assets/index-xNJaUsgv.js",revision:null},{url:"assets/quill-xmFmgOGL.js",revision:null},{url:"index.html",revision:"3b9509622776ae6c4650442f2d88db18"},{url:"registerSW.js",revision:"1872c500de691dce40960bb85481de07"},{url:"pwa-64x64.png",revision:"b8e7916a3e838754fe6d7fe187101348"},{url:"pwa-192x192.png",revision:"b332306616bd7ba215f4b227517debc3"},{url:"pwa-512x512.png",revision:"7bacab3925b9fab8e48b6aec78b9ffa5"},{url:"maskable-icon-512x512.png",revision:"513dfb56fad3a3156e959a2717acfe7d"},{url:"manifest.webmanifest",revision:"16afa9046836f295053ba514fafba085"}],{}),e.cleanupOutdatedCaches(),e.registerRoute(new e.NavigationRoute(e.createHandlerBoundToURL("index.html")))}));
