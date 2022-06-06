<script>
  export let jp_props;
  export let props = {};
  import Dummy from "./Dummy.svelte";
  import Chart from "./Chart.svelte";
  let components = {
                    'Dummy': Dummy,
                    'ChartJS': Chart
                   };
  //event_handler.js requires props
  props['jp_props'] = jp_props;
  
  $:  description_object = {
    style: jp_props.style,
   
  };
  console.log("jp_props");
  console.log(jp_props);
  $: if ('attrs' in jp_props){
   for (const [key, value] of Object.entries(jp_props.attrs)) {
    description_object[key] = value;
  }
  }
  
  $: if (jp_props.classes) {
     description_object['class'] = jp_props.classes
  }
  function dummyEventHandle(event){
  }
  function clickEventHandle(event) {
    eventHandler(props, event, false);
  }
  function inputEventHandle(event){
    eventHandler(props, event, false);
  }
  function changeEventHandle(event){
    eventHandler(props, event, false);
  }
  //for events defined in python -- forward them to eventhandler
  //else use dummyeventhandler
  let click_eh = dummyEventHandle;
  let change_eh = dummyEventHandle;
  let input_eh = dummyEventHandle;  
  if (jp_props.html_tag == 'input'){
    for (let i = 0; i < jp_props.events.length; i++) {
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
    }
    
  }
  else{
    let click_eh = dummyEventHandle;
    if (jp_props.events.length > 0) {
      click_eh = clickEventHandle;
      
    }
  }
</script>

{#if jp_props.vue_type === "html_component"}
  <!-- svelte's syntax for input differs from other html components -->
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

{:else}
  <!-- if component is not a html component; svelte syntax differs for html vs svelte component  -->
  <svelte:component this={components[jp_props.vue_type]}  jp_props={jp_props}/>
{/if}
