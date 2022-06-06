<script>
  import { t } from 'svelte-i18n';
  import Htmlcomponent from './Htmlcomponent.svelte';
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
{#each justpyComponents as jpcomp}
  {#if jpcomp.vue_type === "html_component"}
    <svelte:component this={Htmlcomponent} jp_props={jpcomp}/>
  {:else}
    <svelte:component this={components[jpcomp.vue_type]} jp_props={jpcomp} />
  {/if}
  
  
{/each}


