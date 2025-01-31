<!-- <script lang="ts">
	import { BaseRuntime } from '$lib/baseRuntime';
	import { SceneBuilder } from '$lib/sceneBuilder';
	import { Engine } from "@babylonjs/core/Engines/engine";
	import { onMount } from 'svelte';

  // expose PIXI to window so that this plugin can reference window.PIXI.Ticker
  window.PIXI = PIXI;

  export let data: PageData;

  let container: HTMLElement;
  let modelViewer: HTMLCanvasElement;
  let live2DModel: any;
  let recorder: MediaRecorder | null = null;
  let audioChunks: Blob[] = [];

  SoundManager.volume = 0.9;
  config.logLevel = config.LOG_LEVEL_ERROR;
  config.sound = true;
  config.motionSync = true;

  const cubism4Model = "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display@0.4.0/test/assets/shizuku/shizuku.model.json";

  onMount(() => {
    loadModel();
  });

  async function loadModel() {
    let app = new PIXI.Application({
      view: modelViewer,
      autoStart: true,
      backgroundColor: 0x333333,
      width: container.clientWidth
    });

		BaseRuntime.Create({
				canvas,
				engine,
				sceneBuilder: new SceneBuilder()
		}).then(runtime => runtime.run());
	})
</script> -->


<!-- <div class="container d-flex justify-content-center">
		<div id="sceneElement">

		</div>
</div> -->




<script lang="ts">
	import { onMount } from 'svelte';
	import { createScene } from '$lib/scene';
	import type { PageData } from './$types';
	import { fail } from '@sveltejs/kit';

	export let data: PageData
	let canvas: HTMLCanvasElement;
	let formElement: HTMLFormElement;
	let promptInput: string;
	let isLoading: boolean = false;
	let textAreaEl: HTMLTextAreaElement;

	import { setResponseAnimation } from '$lib/stores';

	onMount(() => {
		createScene(canvas);
	});

	async function initCofig() {
		const response = await fetch("api/v1/init_config");
		
    if(!response.ok) {
      throw fail(response.status, {
        message: response.statusText
      })
    }
		console.log("init_config", await response.json())
	}


	async function initModel() {
		const response = await fetch("api/v1/init_model");
		
    if(!response.ok) {
      throw fail(response.status, {
        message: response.statusText
      })
    }
		console.log("init_model", await response.json())
	}

	async function submitForm() {
		isLoading = true;
		
		let promtJson = {
			prompts: promptInput,
			secret: ""
		}

		let response: Response = await fetch("api/v1/chat_me", {
			method: "POST",
			headers: new Headers({
        'accept': 'application/json',
        'Content-Type': 'application/json'
      }),
			body: JSON.stringify(promtJson)
		});
		
    if(!response.ok) {
      throw fail(response.status, {
        message: response.statusText
      })
    }
		isLoading = false;

		if (!response.body) {
			throw new Error("Response body is nul")
		}
		const reader = response.body.getReader();
		const decoder = new TextDecoder('utf-8');

		let result = '';
		while (true) {
			const { done, value } = await reader.read();

			if (done) break;

			result += decoder.decode(value, { stream: true });
			
			let resultArray: any[] = JSON.parse(result)

			textAreaEl.value = resultArray.join('')
		}

		textAreaEl.style.height = 'auto';
		textAreaEl.style.height = textAreaEl.scrollHeight + 'px';

		setResponseAnimation.set({
			animation_type: "response",
		})

	}

</script>

<svelte:head>
	<title>Babylon.js Sveltekit</title>
	<meta name="description" content="Three.js example app built with Svelte" />
</svelte:head>
<!-- <div role="group">
	<button on:click={initCofig}>INITIALIZE LLM CONFIG</button>
	<button on:click={initModel}>INITIALIZE LLM MODEL</button>
</div> -->
<canvas id="canvas" bind:this={canvas} />

<textarea bind:this={textAreaEl}></textarea>

<form bind:this={formElement}>
  <fieldset role="group">
    <input bind:value={promptInput} name="text" type="text" placeholder="Enter your prompt here" />
    <button disabled={isLoading} on:click={submitForm} type="submit">Submit</button>
    <button>
			<svg class="w-6 h-6 swap-off" fill="none" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
			</svg>
		</button>
  </fieldset>
</form>

<style>
	#canvas {
		display: block;
		width: 100%;
		height: 100%;
	}
</style>
