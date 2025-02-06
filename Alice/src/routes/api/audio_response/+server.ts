import type { RequestHandler } from '../$types';
import { API_URL } from '$env/static/private';

let headerOptions: any = { 'Content-Type': 'application/json; charset=utf-8' };

export const GET: RequestHandler = async ({ fetch, cookies, locals }) => {

  let access_token = locals.access_token

  const response = await fetch(`${API_URL}/audio_response`, {
    method: 'GET',
    headers: new Headers({
      'Accept': 'application/json',
      'Authorization': `Bearer ${access_token}`
    }),
  });

  if (!response.ok) {
    console.log(response);
    return new Response(JSON.stringify(response));
  }
  const data = await response.json();

  console.log(data);

  return new Response(JSON.stringify(data));
};