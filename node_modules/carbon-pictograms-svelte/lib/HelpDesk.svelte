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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V17	c0-0.199,0.161-0.36,0.36-0.36h8.64V16c0-2.415,1.397-4.627,3.535-5.692C12.204,9.485,11.64,8.289,11.64,7	c0-2.404,1.956-4.36,4.36-4.36S20.36,4.596,20.36,7c0,1.289-0.564,2.485-1.535,3.308c2.138,1.064,3.535,3.277,3.535,5.692v0.64H31	c0.199,0,0.36,0.161,0.36,0.36v14C31.36,31.199,31.199,31.36,31,31.36z M1.36,30.64h29.28V17.36H1.36V30.64z M10.36,16.64h11.28V16	c0-2.333-1.471-4.453-3.66-5.275c-0.128-0.048-0.218-0.165-0.231-0.301s0.052-0.269,0.168-0.341C18.995,9.409,19.64,8.257,19.64,7	c0-2.007-1.633-3.64-3.64-3.64S12.36,4.993,12.36,7c0,1.257,0.645,2.409,1.724,3.082c0.116,0.073,0.181,0.205,0.168,0.341	c-0.014,0.136-0.104,0.253-0.232,0.301c-2.189,0.822-3.66,2.942-3.66,5.275C10.36,15.999,10.36,16.64,10.36,16.64z"></path>
</svg>