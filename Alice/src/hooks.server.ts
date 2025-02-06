import type { Handle } from '@sveltejs/kit';
import { API_URL, TOKEN } from '$env/static/private';

export const handle: Handle = async ({ event, resolve }) => {

  event.cookies.set('access_token', TOKEN, {
    path: '/',
    // maxAge: parseInt(decodedToken.exp),
    // secure: true,
    httpOnly: true,
    sameSite: 'none',
    priority: 'high',
    // expires: new Date(decodedToken.exp)
  })

  event.locals.access_token = event.cookies.get('access_token');
  

	const response = await resolve(event);
	return response;
};