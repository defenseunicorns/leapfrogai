<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M22,31.36c-1.853,0-3.36-1.508-3.36-3.36v-9h0.721v9c0,1.456,1.184,2.64,2.64,2.64	s2.64-1.184,2.64-2.64v-5h0.721v5C25.36,29.853,23.853,31.36,22,31.36z M10,31.36c-1.853,0-3.36-1.508-3.36-3.36v-9h0.72v9	c0,1.456,1.185,2.64,2.64,2.64s2.64-1.184,2.64-2.64V4c0-1.853,1.507-3.36,3.36-3.36S19.36,2.147,19.36,4v9h-0.72V4	c0-1.456-1.184-2.64-2.64-2.64S13.36,2.545,13.36,4v24C13.36,29.853,11.853,31.36,10,31.36z M27.255,20.255l-0.51-0.51l3.386-3.385	H16v-0.72h14.131l-3.386-3.386l0.51-0.509L31.509,16L27.255,20.255z M10,16.36H1v-0.72h9V16.36z M7.36,13H6.64V4	c0-1.456-1.185-2.64-2.64-2.64S1.36,2.544,1.36,4v9H0.64V4c0-1.853,1.507-3.36,3.36-3.36S7.36,2.147,7.36,4V13z"></path>
</svg>