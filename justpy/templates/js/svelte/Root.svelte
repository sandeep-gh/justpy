<script>
        import Htmlcomponent  from './Htmlcomponent.svelte';
	export let name;
        export let selected='h2';
        export let imgattr = {id:'myimg', src: "sample.jpg", width:500, height:500, alt:"Girl with Jacket", style:"color:red", title:"this isimag"};
        let jp_props = {html_tag: 'div', text:"i am div", object_props :[]};
        function     handleClick() {
            name = "newname";
            selected = 'h1';
	}
        export let justpycomponents;
</script>

<main>
<svelte:element this={selected}>I'm a {selected} tag</svelte:element>
<svelte:element this='img' {...imgattr}></svelte:element>
<h1>Hello {name}!</h1>

<Htmlcomponent jp_props={jp_props}/>

<button on:click={handleClick}>
	Remove first thing
</button>

</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
