<script lang="ts">
  import type { PageData } from './$types';
  import { Live2DModel, MotionPriority, SoundManager, config } from 'pixi-live2d-display-lipsyncpatch';
  import * as PIXI from 'pixi.js';
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

    live2DModel = await Live2DModel.from(cubism4Model);
    app.stage.addChild(live2DModel);

    live2DModel.scale.set(0.3);
    let centerX = live2DModel.width / 2;
    let container_centerX = container.clientWidth / 2;
    live2DModel.x = live2DModel.x - centerX + container_centerX;

    live2DModel.on('hit', (hitAreaNames: string) => {
      if (hitAreaNames.includes('body')) {
        console.log('hit body');
        var category_name = "idle"; // name of the motion category
        var animation_index = 0; // index of animation under that motion category [null => random]
        var priority_number = 3; // if you want to keep the current animation going or move to new animation by force [0: no priority, 1: idle, 2: normal, 3: forced]
        var audio_link = "https://cdn.jsdelivr.net/gh/RaSan147/pixi-live2d-display@v1.0.3/playground/test.mp3"; //[Optional arg, can be null or empty] [relative or full url path] [mp3 or wav file]
        var volume = 1.0; //[Optional arg, can be null or empty] [0.0 - 1.0]
        var expression = 2; //[Optional arg, can be null or empty] [index|name of expression]
        var resetExpression = true; //[Optional arg, can be null or empty] [true|false] [default: true] [if true, expression will be reset to default after animation is over]

        live2DModel.motion(category_name, animation_index, priority_number, {
          sound: audio_link, 
          volume: volume, 
          expression:expression, 
          resetExpression:resetExpression, 
          crossOrigin : "anonymous"
        })
      }
    });
  }

  // Microphone integration using live2DModel.speak()
  async function startMicrophone() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      console.log('Microphone access granted');
      startRecording(stream);
    } catch (error) {
      console.error('Microphone access denied:', error);
    }
  }

  function startRecording(stream: MediaStream) {
    recorder = new MediaRecorder(stream);
    audioChunks = [];

    recorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    recorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      const base64Audio = await convertBlobToBase64(audioBlob);
      console.log(base64Audio);

      // Pass the Base64 string to live2DModel.speak()
      if (live2DModel) {
        await live2DModel.speak(base64Audio, {
          volume: 1.0
        });
      }
    };

    recorder.start();

    // Automatically stop recording after 5 seconds
    setTimeout(() => {
      recorder?.stop();
    }, 5000); // Stop after 5 seconds
  }

  // Convert Blob to Base64 string
  function convertBlobToBase64(blob: Blob): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }
</script>

<main>
  <div bind:this={container} id="container">
    <button on:click="{startMicrophone}">Start Microphone</button>
    <canvas bind:this={modelViewer} id="modelViewer" style="width: inherit; display: flex; justify-content: center;"></canvas>
  </div>
</main>
