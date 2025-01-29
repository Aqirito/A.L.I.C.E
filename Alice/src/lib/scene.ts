import havokPhysics from "@babylonjs/havok";
import { MmdCamera, MmdMesh, MmdPhysics, MmdRuntime, StreamAudioPlayer, VmdLoader } from "../../node_modules/babylon-mmd";
import { loadAssetContainerAsync, Vector3, HavokPlugin, Scene, Engine, HemisphericLight, DirectionalLight, ShadowGenerator } from "@babylonjs/core";


export const createScene = async (canvas: HTMLCanvasElement) => {
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

  const scene = new Scene(engine);

  scene.enablePhysics(new Vector3(0, -9.8 * 10, 0), new HavokPlugin(true, await havokPhysics()));

  const camera = new MmdCamera("mmdCamera", new Vector3(0, 10, 0), scene);

  const hemisphericLight = new HemisphericLight("HemisphericLight", new Vector3(0, 1, 0), scene);
  hemisphericLight.intensity = 0.3;
  hemisphericLight.specular.set(0, 0, 0);
  hemisphericLight.groundColor.set(1, 1, 1);

  const directionalLight = new DirectionalLight("DirectionalLight", new Vector3(0.5, -1, 1), scene);
  directionalLight.intensity = 0.7;
  directionalLight.shadowMaxZ = 20;
  directionalLight.shadowMinZ = -15;

  const shadowGenerator = new ShadowGenerator(2048, directionalLight, true, camera);
  shadowGenerator.transparencyShadow = true;
  shadowGenerator.bias = 0.01;

  const mmdMesh = await loadAssetContainerAsync("assets/YYB_Hatsune_Miku_10th/YYB_Hatsune_Miku_10th_v1.02.pmx", scene)
    .then((result: any) => {
      console.log("result", result);
      result.addAllToScene();
      return result.meshes[0] as MmdMesh;
    });
  for (const mesh of mmdMesh.metadata.meshes) mesh.receiveShadows = true;
  shadowGenerator.addShadowCaster(mmdMesh);
  
  const mmdRuntime = new MmdRuntime(scene, new MmdPhysics(scene));
  mmdRuntime.register(scene);

  mmdRuntime.setCamera(camera);
  const mmdModel = mmdRuntime.createMmdModel(mmdMesh);

  const audioPlayer = new StreamAudioPlayer(scene);

  const vmdLoader = new VmdLoader(scene);
  const modelMotion = await vmdLoader.loadAsync("model_motion_1", [
    // "assets/メランコリ・ナイト/メランコリ・ナイト.vmd",
    // "assets/メランコリ・ナイト/メランコリ・ナイト_表情モーション.vmd",
    // "assets/メランコリ・ナイト/メランコリ・ナイト_リップモーション.vmd"
    "assets/Intro/1こちら左.vmd" // nice intro
    // "assets/Intro/1ニコ.vmd" // smile intro
    // "assets/Intro/1ホケー.vmd" // angry
    // "assets/Intro/1まったく.vmd" // pissed 2
    // "assets/Intro/1やったー.vmd" // jump happy

  ]);
  // const cameraMotion = await vmdLoader.loadAsync("camera_motion_1",
  //     "assets/メランコリ・ナイト/メランコリ・ナイト_カメラ.vmd"
  // );

  // camera.addAnimation(cameraMotion);
  // camera.setAnimation("camera_motion_1");

  mmdModel.addAnimation(modelMotion);
  mmdModel.setAnimation("model_motion_1");

  const idleMotion1 = await vmdLoader.loadAsync("idle_motion_1", [
    "assets/Idle-Animations-Pack/Air-Scent-Idle-Animation/Smelling-Something-in-the-Air.vmd"
  ]);
  const idleMotion2 = await vmdLoader.loadAsync("idle_motion_2", [
    "assets/Idle-Animations-Pack/Stretching Idle Animation/Stretching.vmd"
  ]);
  const shockMotion1 = await vmdLoader.loadAsync("shock_motion_1", [
    "assets/Intro/1まったく.vmd"
  ]);
  const pissedMotion1 = await vmdLoader.loadAsync("pissed_motion_1", [
    "assets/Intro/1こら.vmd"
  ]);

  setInterval(() => {
    mmdRuntime.setAudioPlayer(null);
    mmdModel.removeAnimation(0);
    const motionList = [idleMotion1, idleMotion2, modelMotion];
    const randomMotion = motionList[Math.floor(Math.random() * motionList.length)];
    mmdModel.addAnimation(randomMotion);

    if (randomMotion == idleMotion1) {
      mmdModel.setAnimation("idle_motion_1");
    }
    if (randomMotion == idleMotion2) {
      mmdModel.setAnimation("idle_motion_2");
    }
    if (randomMotion == modelMotion) {
      mmdModel.setAnimation("model_motion_1");
    }
    mmdRuntime.setManualAnimationDuration(10000);
    mmdRuntime.seekAnimation(0);
    mmdRuntime.playAnimation();
  }, 10000);


  scene.onPointerDown = function (evt, pickResult) {
    console.log(evt);
    if (pickResult.hit) {
      console.log("hit")
      const pickedMesh = pickResult.pickedMesh;
      console.log(pickedMesh)
      if (pickedMesh && pickedMesh.id === "Hair01") {
        playSound("assets/voice-sample.mp3")
        animate(idleMotion2, "idle_motion_2")
      }
      if (pickedMesh && pickedMesh.id === "body01") {
        animate(idleMotion1, "idle_motion_1")
      }
      if (pickedMesh && pickedMesh.id === "q01") {
        animate(pissedMotion1, "pissed_motion_1")
      }
      if (pickedMesh && pickedMesh.id === "q04") {
        animate(shockMotion1, "shock_motion_1")
      }
    }
  };

  function animate(motion: any, motion_name: string) {
    mmdRuntime.setAudioPlayer(null)
    mmdModel.removeAnimation(0)
    mmdModel.addAnimation(motion);
    mmdModel.setAnimation(motion_name);
    mmdRuntime.seekAnimation(0)
    mmdRuntime.playAnimation();
  }

  function playSound(source: string) {
    mmdRuntime.setAudioPlayer(null)
    audioPlayer.source = source;
    mmdRuntime.setAudioPlayer(audioPlayer);
  }

  const headMesh = mmdMesh.getChildMeshes().find(mesh => mesh.id === "face01");
  if (headMesh) {

    headMesh.isPickable = true;
    console.log("face01", headMesh.subMeshes)
    // let bones: any[] = headMesh.skeleton?.bones as any[]
    // const csvContent = bones.map(bone => `${bone.id},${bone.name}`).join("\n");
    // console.log(csvContent)
    // for(let bone of bones) {
    //     // console.log(bone.id, bone.name);

    //     // const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
    //     // const link = document.createElement("a");
    //     // link.href = URL.createObjectURL(blob);
    //     // link.download = "boneData.csv";
    //     // link.click();
    // }
  }


  mmdRuntime.playAnimation();

  engine.runRenderLoop(() => {
    scene.render();
  });

  window.addEventListener('resize', () => {
    engine.resize();
  });

  return scene;
}