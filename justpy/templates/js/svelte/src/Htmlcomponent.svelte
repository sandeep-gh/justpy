<script>
  export let jp_props;
  export let props = {};

  //align with event handler
  props['jp_props'] = jp_props;
  
  let description_object = {
    style: jp_props.style,
   
  };
  console.log("debug attrs");
  for (const [key, value] of Object.entries(jp_props.attrs)) {
    console.log(key, value);
    description_object[key] = value;
  }
  //attrs: JSON.stringify(jp_props['attrs'])
  console.log("style and attrs");
  console.log(jp_props['style']);
  console.log(JSON.stringify(jp_props['attrs']));  

  
  if (jp_props.classes) {
    description_object['class'] = jp_props.classes
  }

  
  function dummyEventHandle(event){
    console.log("from dummyeventhandle");
  }
  function clickEventHandle(event) {
    // eventHandler(this.$props, event, false);
    console.log("from handleClickEvent");
    eventHandler(props, event, false);
  }
  function inputEventHandle(event){
    console.log("inputEventHandle called");
    eventHandler(props, event, false);
  }
  function changeEventHandle(event){
    console.log("changeEventHandle called");
    eventHandler(props, event, false);
  }
  let click_eh = dummyEventHandle;
  let change_eh = dummyEventHandle;
  let input_eh = dummyEventHandle;  
  if (jp_props.html_tag == 'input'){
    for (let i = 0; i < jp_props.events.length; i++) {
      console.log("i can iterate");
      switch(jp_props.events[i]) {
      case "before":
        console.log("before event not implemented");
        break;
      case "input":
        input_eh = inputEventHandle;
        break;
      case "change":
        change_eh = changeEventHandle;
        break;
      }
      console.log(jp_props.events[i]);
    }
    
  }
  else{
    let click_eh = dummyEventHandle;
    if (jp_props.events.length > 0) {
      console.log("assuming first event is a click event");
      click_eh = clickEventHandle;
      
    }
  }
</script>

{#if jp_props.html_tag === "input"}
  <input  {...description_object} on:input={input_eh} on:change={change_eh}>
{:else}
  <svelte:element this={jp_props.html_tag} {...description_object} on:click={click_eh}>
    {#if jp_props.text}
      {jp_props.text}
    {/if}
    
    {#each jp_props.object_props as cobj_props}
      {#if cobj_props.show}
        <svelte:self jp_props={cobj_props}/>
      {/if}
    {/each}

      </svelte:element>
    {/if}    
