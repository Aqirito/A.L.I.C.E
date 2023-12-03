
export const prerender = true
export const ssr = false

import type { LayoutLoad } from './$types';

export const load = (async () => {
    return {};
}) satisfies LayoutLoad;