<script>
  import { t } from 'svelte-i18n';
  import Htmlcomponent from './Htmlcomponent.svelte';

  export let name;

  export let justpyComponents;
  
</script>
{#each justpyComponents as jpcomp}
  <Htmlcomponent jp_props={jpcomp}/>
{/each}


