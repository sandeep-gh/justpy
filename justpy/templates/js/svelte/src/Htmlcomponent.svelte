<script>
  export let jp_props;
  let description_object = {
    style: jp_props.style,
    attrs: jp_props.attrs
  };
  if (jp_props.classes) {
    description_object['class'] = jp_props.classes
  }
  console.log(description_object);
  console.log("from htmlcomponents");
  console.log(jp_props);
  console.log("hello");
</script>


<svelte:element this={jp_props.html_tag} {...description_object}>
{#if jp_props.text}
{jp_props.text}
{/if}
{#each jp_props.object_props as cobj_props}
{#if cobj_props.show}
<svelte:self jp_props={cobj_props}/>
{/if}
{/each}

</svelte:element>
