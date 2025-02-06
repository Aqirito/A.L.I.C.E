// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			user: any,
			access_token: any
		}
		// interface PageData {}
		// interface Platform {}
	}
  interface Window {
    PIXI: any;
  }
}
export {};
