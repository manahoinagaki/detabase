(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/frontend/node_modules/next/dist/compiled/react-refresh/cjs/react-refresh-runtime.development.js [app-client] (ecmascript)", (() => {{

throw new Error("An error occurred while generating the chunk item [project]/frontend/node_modules/next/dist/compiled/react-refresh/cjs/react-refresh-runtime.development.js [app-client] (ecmascript)\n\nCaused by:\n- the chunking context (unknown) does not support external modules (request: node:process)\n\nDebug info:\n- An error occurred while generating the chunk item [project]/frontend/node_modules/next/dist/compiled/react-refresh/cjs/react-refresh-runtime.development.js [app-client] (ecmascript)\n- Execution of <ModuleChunkItem as EcmascriptChunkItem>::content_with_async_module_info failed\n- Execution of *EcmascriptChunkItemContent::new failed\n- Execution of EcmascriptModuleContent::new failed\n- the chunking context (unknown) does not support external modules (request: node:process)");

}}),
"[project]/frontend/node_modules/next/dist/compiled/react-refresh/runtime.js [app-client] (ecmascript)", (() => {{

throw new Error("An error occurred while generating the chunk item [project]/frontend/node_modules/next/dist/compiled/react-refresh/runtime.js [app-client] (ecmascript)\n\nCaused by:\n- the chunking context (unknown) does not support external modules (request: node:process)\n\nDebug info:\n- An error occurred while generating the chunk item [project]/frontend/node_modules/next/dist/compiled/react-refresh/runtime.js [app-client] (ecmascript)\n- Execution of <ModuleChunkItem as EcmascriptChunkItem>::content_with_async_module_info failed\n- Execution of *EcmascriptChunkItemContent::new failed\n- Execution of EcmascriptModuleContent::new failed\n- the chunking context (unknown) does not support external modules (request: node:process)");

}}),
"[project]/frontend/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/runtime.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __importDefault = /*TURBOPACK member replacement*/ __turbopack_context__.e && /*TURBOPACK member replacement*/ __turbopack_context__.e.__importDefault || function(mod) {
    return mod && mod.__esModule ? mod : {
        "default": mod
    };
};
Object.defineProperty(exports, "__esModule", {
    value: true
});
const runtime_1 = __importDefault(__turbopack_context__.r("[project]/frontend/node_modules/next/dist/compiled/react-refresh/runtime.js [app-client] (ecmascript)"));
const helpers_1 = __importDefault((()=>{
    const e = new Error("Cannot find module './internal/helpers'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})());
// Hook into ReactDOM initialization
runtime_1.default.injectIntoGlobalHook(self);
// Register global helpers
self.$RefreshHelpers$ = helpers_1.default;
// Register a helper for module execution interception
self.$RefreshInterceptModuleExecution$ = function(webpackModuleId) {
    var prevRefreshReg = self.$RefreshReg$;
    var prevRefreshSig = self.$RefreshSig$;
    self.$RefreshReg$ = function(type, id) {
        runtime_1.default.register(type, webpackModuleId + ' ' + id);
    };
    self.$RefreshSig$ = runtime_1.default.createSignatureFunctionForTransform;
    // Modeled after `useEffect` cleanup pattern:
    // https://react.dev/learn/synchronizing-with-effects#step-3-add-cleanup-if-needed
    return function() {
        self.$RefreshReg$ = prevRefreshReg;
        self.$RefreshSig$ = prevRefreshSig;
    };
}; //# sourceMappingURL=runtime.js.map
}),
]);

//# sourceMappingURL=9e883_next_dist_compiled_acc558a9._.js.map