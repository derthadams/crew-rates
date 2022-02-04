import { rest } from "msw";
import { pro, bur, end, dis, details, cam } from "./responses";

export const handlers = [
    rest.get("/api/shows/", (req, res, ctx) => {
        const q = req.url.searchParams.get("q");

        if (q === "Pro") {
            return res(ctx.json(pro));
        } else {
            return res(ctx.json([]))
        }
    }),
    rest.get("api/companies/", (req, res, ctx) => {
        const q = req.url.searchParams.get("q");

        if (q === "End") {
            return res(ctx.json(end));
        } else {
            return res(ctx.json([]))
        }
    }),
    rest.get("api/networks/", (req, res, ctx) => {
        const q = req.url.searchParams.get("q");

        if (q === "Dis") {
            return res(ctx.json(dis));
        } else {
            return res(ctx.json([]))
        }
    }),
    rest.get("api/autocomplete/", (req, res, ctx) => {
        const q = req.url.searchParams.get("q");

        if (q === "Bur") {
            return res(ctx.json(bur));
        }
    }),
    rest.get("api/details/", (req, res, ctx) => {
        const q = req.url.searchParams.get("q");

        if (q === "ChIJlcUYKBWVwoAR1IofkK-RdzA") {
            return res(ctx.json(details));
        }
    }),
    rest.get("api/job-titles/", (req, res, ctx) => {
        const q = req.url.searchParams.get("q");

        if (q === "Cam") {
            return res(ctx.json(cam));
        }
    })
];
