<script lang="ts">
	import Navbar from '$lib/Navbar.svelte';
    import type { LayoutData } from './$types';
    
    export let data: LayoutData;
</script>
<div class="container">
  <Navbar/>
  <slot />
</div>