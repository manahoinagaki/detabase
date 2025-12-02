(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/frontend/components/MapCard.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// \frontend\Alternative_data_frontend\frontend\components\MapCard.tsx
__turbopack_context__.s([
    "default",
    ()=>MapCard
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$MapContainer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/react-leaflet/lib/MapContainer.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$TileLayer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/react-leaflet/lib/TileLayer.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$CircleMarker$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/react-leaflet/lib/CircleMarker.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Tooltip$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/react-leaflet/lib/Tooltip.js [app-client] (ecmascript)");
"use client";
;
;
function MapCard({ geo }) {
    const center = [
        35.6812,
        139.7671
    ];
    const features = geo?.features ?? [];
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$MapContainer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["MapContainer"], {
        center: center,
        zoom: 5,
        scrollWheelZoom: false,
        style: {
            height: "100%",
            width: "100%",
            borderRadius: "1rem"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$TileLayer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TileLayer"], {
                attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            }, void 0, false, {
                fileName: "[project]/frontend/components/MapCard.tsx",
                lineNumber: 12,
                columnNumber: 7
            }, this),
            features.map((f, idx)=>{
                const [lng, lat] = f.geometry.coordinates;
                const activity = f.properties.activity ?? 50;
                const radius = Math.max(8, Math.min(24, activity / 3));
                return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$CircleMarker$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CircleMarker"], {
                    center: [
                        lat,
                        lng
                    ],
                    radius: radius,
                    pathOptions: {
                        color: "#10a8dc"
                    },
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Tooltip$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Tooltip"], {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                fontSize: 12
                            },
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: f.properties.name
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/components/MapCard.tsx",
                                        lineNumber: 24,
                                        columnNumber: 22
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/frontend/components/MapCard.tsx",
                                    lineNumber: 24,
                                    columnNumber: 17
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: [
                                        "Activity: ",
                                        activity
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/frontend/components/MapCard.tsx",
                                    lineNumber: 25,
                                    columnNumber: 17
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/frontend/components/MapCard.tsx",
                            lineNumber: 23,
                            columnNumber: 15
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/frontend/components/MapCard.tsx",
                        lineNumber: 22,
                        columnNumber: 13
                    }, this)
                }, idx, false, {
                    fileName: "[project]/frontend/components/MapCard.tsx",
                    lineNumber: 21,
                    columnNumber: 11
                }, this);
            })
        ]
    }, void 0, true, {
        fileName: "[project]/frontend/components/MapCard.tsx",
        lineNumber: 11,
        columnNumber: 5
    }, this);
}
_c = MapCard;
var _c;
__turbopack_context__.k.register(_c, "MapCard");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/frontend/components/MapCard.tsx [app-client] (ecmascript, next/dynamic entry)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/frontend/components/MapCard.tsx [app-client] (ecmascript)"));
}),
"[project]/frontend/node_modules/react-leaflet/lib/MapContainer.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "MapContainer",
    ()=>MapContainer
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
;
;
function MapContainerComponent({ bounds, boundsOptions, center, children, className, id, placeholder, style, whenReady, zoom, ...options }, forwardedRef) {
    const [props] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        className,
        id,
        style
    });
    const [context, setContext] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const mapInstanceRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(undefined);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useImperativeHandle"])(forwardedRef, {
        "MapContainerComponent.useImperativeHandle": ()=>context?.map ?? null
    }["MapContainerComponent.useImperativeHandle"], [
        context
    ]);
    // biome-ignore lint/correctness/useExhaustiveDependencies: ref callback
    const mapRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "MapContainerComponent.useCallback[mapRef]": (node)=>{
            if (node !== null && !mapInstanceRef.current) {
                const map = new LeafletMap(node, options);
                mapInstanceRef.current = map;
                if (center != null && zoom != null) {
                    map.setView(center, zoom);
                } else if (bounds != null) {
                    map.fitBounds(bounds, boundsOptions);
                }
                if (whenReady != null) {
                    map.whenReady(whenReady);
                }
                setContext(createLeafletContext(map));
            }
        }
    }["MapContainerComponent.useCallback[mapRef]"], []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "MapContainerComponent.useEffect": ()=>{
            return ({
                "MapContainerComponent.useEffect": ()=>{
                    context?.map.remove();
                }
            })["MapContainerComponent.useEffect"];
        }
    }["MapContainerComponent.useEffect"], [
        context
    ]);
    const contents = context ? /*#__PURE__*/ __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].createElement(LeafletContext, {
        value: context
    }, children) : placeholder ?? null;
    return /*#__PURE__*/ __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].createElement("div", {
        ...props,
        ref: mapRef
    }, contents);
}
const MapContainer = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["forwardRef"])(MapContainerComponent);
}),
"[project]/frontend/node_modules/react-leaflet/lib/TileLayer.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "TileLayer",
    ()=>TileLayer
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
;
const TileLayer = createTileLayerComponent(function createTileLayer({ url, ...options }, context) {
    const layer = new LeafletTileLayer(url, withPane(options, context));
    return createElementObject(layer, context);
}, function updateTileLayer(layer, props, prevProps) {
    updateGridLayer(layer, props, prevProps);
    const { url } = props;
    if (url != null && url !== prevProps.url) {
        layer.setUrl(url);
    }
});
}),
"[project]/frontend/node_modules/react-leaflet/lib/CircleMarker.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CircleMarker",
    ()=>CircleMarker
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
;
const CircleMarker = createPathComponent(function createCircleMarker({ center, children: _c, ...options }, ctx) {
    const marker = new LeafletCircleMarker(center, options);
    return createElementObject(marker, extendContext(ctx, {
        overlayContainer: marker
    }));
}, updateCircle);
}),
"[project]/frontend/node_modules/react-leaflet/lib/Tooltip.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Tooltip",
    ()=>Tooltip
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
;
;
const Tooltip = createOverlayComponent(function createTooltip(props, context) {
    const tooltip = new LeafletTooltip(props, context.overlayContainer);
    return createElementObject(tooltip, context);
}, function useTooltipLifecycle(element, context, { position }, setOpen) {
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])(function addTooltip() {
        const container = context.overlayContainer;
        if (container == null) {
            return;
        }
        const { instance } = element;
        const onTooltipOpen = {
            "Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipOpen": (event)=>{
                if (event.tooltip === instance) {
                    if (position != null) {
                        instance.setLatLng(position);
                    }
                    instance.update();
                    setOpen(true);
                }
            }
        }["Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipOpen"];
        const onTooltipClose = {
            "Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipClose": (event)=>{
                if (event.tooltip === instance) {
                    setOpen(false);
                }
            }
        }["Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipClose"];
        container.on({
            tooltipopen: onTooltipOpen,
            tooltipclose: onTooltipClose
        });
        container.bindTooltip(instance);
        return function removeTooltip() {
            container.off({
                tooltipopen: onTooltipOpen,
                tooltipclose: onTooltipClose
            });
            // @ts-ignore protected property
            if (container._map != null) {
                container.unbindTooltip();
            }
        };
    }, [
        element,
        context,
        setOpen,
        position
    ]);
});
}),
]);

//# sourceMappingURL=frontend_d2bf4410._.js.map