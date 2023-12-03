<script lang="ts">
	import type { PageData } from './$types';
	import * as PIXI from 'pixi.js';
	import { Live2DModel, MotionPriority, SoundManager, config } from 'pixi-live2d-display';

	import { onMount } from 'svelte';

	export let data: PageData;

  let container: any = null;
  // expose PIXI to window so that this plugin is able to
  // reference window.PIXI.Ticker to automatically update Live2D models
  window.PIXI = PIXI;
  let audio: any;

  SoundManager.volume = 0.2;
  // SoundManager.add('Resources/Haru/sound/006.wav');
  // log level
  config.logLevel = config.LOG_LEVEL_ERROR; // LOG_LEVEL_VERBOSE, LOG_LEVEL_ERROR, LOG_LEVEL_NONE

  // play sound for motions
  config.sound = true;

  // defer the playback of a motion and its sound until both are loaded
  config.motionSync = true;

  config.cubism4.supportMoreMaskDivisions = true;

  const cubism4Model =
  "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json";

  onMount(() => {
    loadModel();
  });

	async function loadModel() {
		let app = new PIXI.Application({
			view: document.getElementById('canvas') as HTMLCanvasElement,
      autoStart: true,
      resizeTo: container,
      backgroundColor: 0x333333,
      width: container.clientWidth,
      forceCanvas: true
		});

		let model: Live2DModel = await Live2DModel.from('Resources/Mao/Mao.model3.json', {idleMotionGroup: 'Idle', autoInteract: false});
		// let model: any = await Live2DModel.from(cubism4Model);

    model.on('hit', (hitAreaNames: string) => {
      if (hitAreaNames.includes('Body')) {
        // body is hit
        model.motion('TapBody', undefined, MotionPriority.FORCE)
        // model.motion('TapBody')
        model.expression()
        
        SoundManager.play(audio);
      }
    });
    model.on('hit', (hitAreaNames: string) => {
      if (hitAreaNames.includes('Head')) {
        model.expression()
      }
    });
    app.stage.addChild(model);

		model.scale.set(0.1);
    let centerX = model.width / 2;
    // console.log("centerX",centerX)
    let container_centerX = container.clientWidth / 2;
    // console.log("container_centerX",container_centerX)
    model.x = (model.x - centerX) + container_centerX
    // console.log("model.x",model.x)
	}
</script>


<main bind:this={container} class="container">
  <audio bind:this={audio} controls>
    <source src="006.wav" type="audio/wav">
    Your browser does not support the audio element.
  </audio>
  <canvas id="canvas" style="width: inherit; display: flex; justfy-content: center"></canvas>
</main>