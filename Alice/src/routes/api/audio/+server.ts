import type { RequestHandler } from '../$types';
import { API_URL } from '$env/static/private';

let headerOptions: any = { 'Content-Type': 'application/json; charset=utf-8' };

export const GET: RequestHandler = async ({ fetch, cookies, locals }) => {

  let access_token = locals.access_token

  const result = await fetch(`${API_URL}/audio`, {
    method: 'GET',
    headers: new Headers({
      'Accept': 'application/octet-stream',
      'Authorization': `Bearer ${access_token}`
    }),
  });

  if (!result.ok) {
    console.log(result);
    return new Response(JSON.stringify(result));
  }
  const data = await result.blob();


  return new Response(data);
};