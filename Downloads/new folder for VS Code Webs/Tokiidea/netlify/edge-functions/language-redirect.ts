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

const languageCookie = (language: "en" | "sl", domain: string) =>
    `tokiidea-language=${language}; Domain=${domain}; Path=/; Max-Age=31536000; SameSite=Lax; Secure`;

const redirect = (url: URL, cookie?: string) =>
    new Response(null, {
        status: 302,
        headers: {
            "Location": url.toString(),
            "Cache-Control": "no-store",
            ...(cookie ? { "Set-Cookie": cookie } : {})
        }
    });

export default async (request: Request, context: Context) => {
    if (request.method !== "GET" || !request.headers.get("accept")?.includes("text/html")) {
        return context.next();
    }

    const url = new URL(request.url);
    const hostname = url.hostname.toLowerCase();
    const isSlovenianDomain = hostname === "tokiidea.si" || hostname === "www.tokiidea.si";
    const isEnglishDomain = hostname === "tokiidea.com" || hostname === "www.tokiidea.com";
    if (!isSlovenianDomain && !isEnglishDomain) {
        return context.next();
    }

    const requestedLanguage = url.searchParams.get("tokiidea_language");
    const languageChoice = requestedLanguage === "en" || requestedLanguage === "sl"
        ? requestedLanguage
        : undefined;
    if (languageChoice) {
        url.searchParams.delete("tokiidea_language");
    }

    const path = url.pathname === "/" ? "/index.html" : url.pathname;
    const isSlovenianPath = path.startsWith("/sl/");
    const englishPath = isSlovenianPath ? path.slice(3) : path;
    if (!translatedPages.has(englishPath)) {
        return context.next();
    }

    if (isSlovenianDomain) {
        if (languageChoice) {
            return redirect(url, languageCookie(languageChoice, "tokiidea.si"));
        }
        if (isSlovenianPath) return context.next();
        url.pathname = `/sl${englishPath}`;
        return url;
    }

    if (languageChoice === "en") {
        return redirect(url, languageCookie("en", "tokiidea.com"));
    }

    const cookie = request.headers.get("cookie") ?? "";
    const preference = cookie.match(/(?:^|;\s*)tokiidea-language=(en|sl)(?:;|$)/)?.[1];
    const shouldUseSlovenian = languageChoice === "sl" ||
        preference === "sl" ||
        (!preference && context.geo.country?.code === "SI");

    if (shouldUseSlovenian) {
        const destination = new URL(url);
        destination.hostname = "tokiidea.si";
        destination.protocol = "https:";
        destination.pathname = englishPath;
        if (languageChoice === "sl") {
            destination.searchParams.set("tokiidea_language", "sl");
        }
        return redirect(destination);
    }

    if (isSlovenianPath) {
        url.pathname = englishPath;
        return redirect(url);
    }

    return context.next();
};
