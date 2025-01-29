import { PUBLIC_API_URL } from '$env/static/public';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ fetch, request }) => {
  const resultFetched = await request.json();

  const res = await fetch(`http://localhost:8000/llm/chat`,
    {
      method: 'POST',
      headers: new Headers({
        'accept': 'application/json',
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify(resultFetched)
    }
  );

  if (!res.ok) {
    console.error(`Error: ${res.status} ${res.statusText}`);
    console.error(`Response Headers: ${JSON.stringify([...res.headers])}`);
    const responseBody = await res.text();
    console.error(`Response Body: ${responseBody}`);

    const response = new Response(responseBody, {
      status: res.status,
      statusText: res.statusText,
      headers: res.headers
    });
    return response;
  }

  const results = await res.json();
  console.log("DDFF", results);

  return new Response(JSON.stringify(results));
};