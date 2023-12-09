import * as fs from 'node:fs'

let Pe, qt;
const Qe = new Array(128).fill(void 0);
Qe.push(void 0, null, !0, !1);
let Gt = Qe.length;

// --- tool func start ---
const $i = typeof TextDecoder < 'u' ? new TextDecoder('utf-8', {
  ignoreBOM: !0,
  fatal: !0
}) : {
  decode: () => {
    throw Error('TextDecoder not available')
  }
};
let Tr = 0,
  Wt = null;
function qu(e) {
  const t = Ar(e);
  return Wu(e),
    t
}
function On() {
  return (Wt === null || Wt.byteLength === 0) &&
    (Wt = new Uint8Array(Pe.memory.buffer)),
    Wt
}
function Ku(e, t, n) {
  if (n === void 0) {
    const l = Sn.encode(e),
      c = t(l.length, 1) >>> 0;
    return On().subarray(c, c + l.length).set(l),
      Tr = l.length,
      c
  }
  let r = e.length,
    s = t(r, 1) >>> 0;
  const o = On();
  let i = 0;
  for (; i < r; i++) {
    const l = e.charCodeAt(i);
    if (l > 127) break;
    o[s + i] = l
  }
  if (i !== r) {
    i !== 0 &&
      (e = e.slice(i)),
      s = n(s, r, r = i + e.length * 3, 1) >>> 0;
    const l = On().subarray(s + i, s + r),
      c = Uu(e, l);
    i += c.written
  }
  return Tr = i,
    s
}
function Ar(e) {
  return Qe[e]
}
function Vu(e) {
  return e == null
}
function Wu(e) {
  e < 132 ||
    (Qe[e] = Gt, Gt = e)
}
function Di(e, t) {
  return e = e >>> 0,
    $i.decode(On().subarray(e, e + t))
}
// --- tool func end ---
function jn() {
  return (qt === null || qt.byteLength === 0) &&
    (qt = new Int32Array(Pe.memory.buffer)),
    qt
}
/**
* wasm pure function
 */
function Ma(e) {
  return Pe.o(e) >>> 0
}
function Bi(e) {
  Gt === Qe.length &&
    Qe.push(Qe.length + 1);
  const t = Gt;
  return Gt = Qe[t],
    Qe[t] = e,
    t
}
/**
* wasm pure function
 */
function La(e, t) {
  try {
    const s = Pe.__wbindgen_add_to_stack_pointer(- 16);
    Pe.f(s, e, Bi(t));
    var n = jn()[s / 4 + 0],
      r = jn()[s / 4 + 1];
    let o;
    return n !== 0 &&
      (o = Di(n, r).slice(), Pe.__wbindgen_free(n, r * 1, 1)),
      o
  } finally {
    Pe.__wbindgen_add_to_stack_pointer(16)
  }
}
// ---- wasm begin ---
/**
 * pure function
 */
async function zu(e, t) {
  if (typeof Response == 'function' && e instanceof Response) {
    if (typeof WebAssembly.instantiateStreaming == 'function') try {
      return await WebAssembly.instantiateStreaming(e, t)
    } catch (r) {
      if (e.headers.get('Content-Type') != 'application/wasm') console.warn(
        '`WebAssembly.instantiateStreaming` failed because your server does not serve wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n',
        r
      );
      else throw r
    }
    const n = await e.arrayBuffer();
    return await WebAssembly.instantiate(n, t)
  } else {
    const n = await WebAssembly.instantiate(e, t);
    return n instanceof WebAssembly.Instance ? {
      instance: n,
      module: e
    }
      : n
  }
}
/**
 * pure function
 */
function Qu() {
  const e = {};
  return e.wbg = {},
    e.wbg.__wbindgen_string_get = function (t, n) {
      const r = Ar(n),
        s = typeof r == 'string' ? r : void 0;
      var o = Vu(s) ? 0 : Ku(s, Pe.__wbindgen_malloc, Pe.__wbindgen_realloc),
        i = Tr;
      jn()[t / 4 + 1] = i,
        jn()[t / 4 + 0] = o
    },
    e.wbg.__wbindgen_object_drop_ref = function (t) {
      qu(t)
    },
    e.wbg.__wbg_getTime_ed6ee333b702f8fc = function (t) {
      return Ar(t).getTime()
    },
    e.wbg.__wbg_new0_ad75dd38f92424e2 = function () {
      return Bi(new Date)
    },
    e.wbg.__wbindgen_throw = function (t, n) {
      throw new Error(Di(t, n))
    },
    e
}
function Yu(e, t) {
  return Pe = e.exports,
    Hi.__wbindgen_wasm_module = t,
    qt = null,
    Wt = null,
    Pe
}
/**
 * main entry
 */
async function Hi(e) {
  if (Pe !== void 0) return Pe;
  typeof e > 'u' &&
    (
      e = await new Promise((res, rej) => {
        fs.readFile('./plugins/ba_query/yuyuko.wasm', (e, d) => e ? rej(e) : res(d))
      })
    );
  const t = Qu();
  (
    typeof e == 'string' ||
    typeof Request == 'function' &&
    e instanceof Request ||
    typeof URL == 'function' &&
    e instanceof URL
  )
  const {
    instance: n,
    module: r
  }
    = await zu(await e, t);
  return Yu(n, r)
}
// ---- wasm end ---
/** entry, Lu is createVueApp, na is router, Fu() is pinia */
// Hi().then(e => {
// const t = Lu(Gf);
// t.use(Fu()),
//   t.use(na),
//   t.mount('#app')
// });
const dec = e => La(Ma(2), e)
export {
  dec,
  Hi as init
};
