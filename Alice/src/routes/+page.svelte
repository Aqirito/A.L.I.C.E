<script lang="ts">
	import { BaseRuntime } from '$lib/baseRuntime';
	import { SceneBuilder } from '$lib/sceneBuilder';
	import { Engine } from "@babylonjs/core/Engines/engine";
	import { onMount } from 'svelte';


	onMount(()=> {

		const canvas = document.createElement("canvas");
		const sceneElement = document.getElementById("sceneElement") as HTMLDivElement;
		canvas.style.width = "100%";
		canvas.style.height = "100%";
		canvas.style.display = "block";
		sceneElement.appendChild(canvas);



		const engine = new Engine(canvas, false, {
				preserveDrawingBuffer: false,
				stencil: true,
				antialias: true,
				alpha: true,
				premultipliedAlpha: false,
				powerPreference: "high-performance",
				doNotHandleTouchAction: false,
				doNotHandleContextLost: true,
				audioEngine: true,
				adaptToDeviceRatio: true,
				useHighPrecisionMatrix: true,
				useHighPrecisionFloats: true
		}, true);


		BaseRuntime.Create({
				canvas,
				engine,
				sceneBuilder: new SceneBuilder()
		}).then(runtime => runtime.run());
	})
</script>


<div class="container d-flex justify-content-center">
		<div id="sceneElement">

		</div>
</div>