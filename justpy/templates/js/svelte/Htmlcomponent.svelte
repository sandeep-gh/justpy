<script>
        export let jp_props;
        let  tag = jp_props.html_tag;
        let description_object = {style:jp_props.style};
</script>


<svelte:element this={jp_props.html_tag} {...description_object}>
{#if jp_props.text}
{jp_props.text}
{/if}
{#each jp_props.object_props as cobj_props}
{#if cobj_props.show}
<svelte:self cobj_props/>
{/if}
{/each}

</svelte:element>
