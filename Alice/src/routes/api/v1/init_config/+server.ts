import { PUBLIC_API_URL } from '$env/static/public';
import type { RequestHandler } from '../$types';

export const GET: RequestHandler = async ({ fetch }) => {

  const response = await fetch(`${PUBLIC_API_URL}/init/configs`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  if (!response.ok) {
    return new Response(
      JSON.stringify({
        success: false,
        message: response.statusText
      })
    )
  }

  const profile = await response.json();

  return new Response(JSON.stringify(profile));
};