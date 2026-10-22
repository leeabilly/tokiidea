import type { Context } from "@netlify/edge-functions";

const translatedPages = new Set([
    "/index.html",
    "/product.html",
    "/cart.html",
    "/contact.html",
    "/faq.html",
    "/shipping.html",
    "/returns.html",
    "/privacy.html",
    "/terms.html",
    "/cookies.html",
    "/success.html"
]);

export default async (request: Request, context: Context) => {
    if (request.method !== "GET" || !request.headers.get("accept")?.includes("text/html")) {
        return context.next();
    }

    const url = new URL(request.url);
    const path = url.pathname === "/" ? "/index.html" : url.pathname;
    const cookie = request.headers.get("cookie") ?? "";
    const preference = cookie.match(/(?:^|;\s*)tokiidea-language=(en|sl)(?:;|$)/)?.[1];
    const language = preference ?? (context.geo.country?.code === "SI" ? "sl" : undefined);
    const isSlovenianPage = path.startsWith("/sl/");
    const englishPage = isSlovenianPage ? path.slice(3) : path;

    if (!language || !translatedPages.has(englishPage)) {
        return context.next();
    }

    const destination = language === "sl"
        ? (isSlovenianPage ? undefined : `/sl${englishPage}`)
        : (isSlovenianPage ? englishPage : undefined);

    if (!destination || destination === url.pathname) {
        return context.next();
    }

    url.pathname = destination;
    return new Response(null, {
        status: 302,
        headers: {
            "Location": url.toString(),
            "Cache-Control": "no-store"
        }
    });
};
