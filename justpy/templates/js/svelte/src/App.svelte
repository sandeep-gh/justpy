<script>
  export let name;


  var btncolor = "bg-green-200/50";
  function on_click(event){
    console.log("on click called");
    btncolor = "bg-pink-200/50";
  }

  import Htmlcomponent from './Htmlcomponents.svelte';
  import Dummy from "./Dummy.svelte";
  import Chart from "./Chart.svelte";
  export let justpyComponents;
  let dummy_props = {};
  let selected_component = Htmlcomponent;
  let components = {'html_component': Htmlcomponent,
                    'Dummy': Dummy,
                    'ChartJS': Chart
                   };
</script>

<!-- <main class="text-center py-12 max-w-xs mx-auto sm:max-w-none"> -->
<!--   <h1 class="text-red-400 text-6xl uppercase leading-loose font-thin">Hello {name}!</h1> -->
<!--   <p class="text-stone-700 mt-4"> -->
<!--     Visit the <a class="text-sky-600 hover:underline" href="https://svelte.dev/tutorial"> -->
<!--     Svelte tutorial</a> to learn how to build Svelte apps. -->
<!--   </p> -->
<!--   <button class={btncolor} on:click={on_click}> -->
<!--     clickme -->
<!--     </button> -->
<!-- </main> -->
{#each justpyComponents as jpcomp}
  {#if jpcomp.vue_type === "html_component"}
    <svelte:component this={Htmlcomponent} jp_props={jpcomp}/>
  {:else}
    <svelte:component this={components[jpcomp.vue_type]} jp_props={jpcomp} />
  {/if}
  
  
{/each}


<style lang="postcss" global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
