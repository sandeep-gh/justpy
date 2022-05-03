<script>
        import Htmlcomponent  from './Htmlcomponent.svelte';
	export let name;
        export let justpyComponents;    
        export let selected='h2';
        export let imgattr = {id:'myimg', src: "sample.jpg", width:500, height:500, alt:"Girl with Jacket", style:"color:red", title:"this isimag"};
        let jp_props = {html_tag: 'div', text:"i am div", object_props :[]};
        function     handleClick() {
            name = "newname";
            selected = 'h1';
                    console.log(justpyComponents);
	}


</script>

<main>
<svelte:element this={selected}>I'm a {selected} tag</svelte:element>
<svelte:element this='img' {...imgattr}></svelte:element>
<h1>Hello {name}!</h1>
{#each justpyComponents as jpc}
<Htmlcomponent jp_props={jpc}/>
{/each}

<Htmlcomponent jp_props={jp_props}/>

<button on:click={handleClick}>
	Remove first thing
</button>

</main>


<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
    
