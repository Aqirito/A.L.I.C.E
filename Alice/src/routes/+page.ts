import type { PageLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';
import { fail } from '@sveltejs/kit';

export const load = (async () => {

  return {
  }
}) satisfies PageLoad;