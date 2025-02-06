import type { RequestHandler } from './$types';
import { API_URL } from '$env/static/private';

export const GET: RequestHandler = async () => {
    return new Response();
};

export const POST: RequestHandler = async ({ fetch, locals, request }) => {
    let access_token = locals.access_token

    let headerOptions: any = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'Authorization': `Bearer ${access_token}`
    
    };

    const prompts = await request.json();

    const result = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: new Headers(headerOptions),
      body: JSON.stringify(prompts)
    });
    if (!result.ok) {
      return new Response(JSON.stringify(result));
    }
    return new Response(
      JSON.stringify(
        await result.json()
      )
    );
  }