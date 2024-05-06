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
  <path d="M27,31.36H3c-1.301,0-2.36-1.059-2.36-2.36V5c0-1.301,1.059-2.36,2.36-2.36h13v0.72H3 C2.096,3.36,1.36,4.096,1.36,5v24c0,0.904,0.736,1.64,1.64,1.64h24c0.904,0,1.64-0.735,1.64-1.64V16h0.721v13 C29.36,30.302,28.302,31.36,27,31.36z M23,18.36h-9.36V9h0.72v8.131L30.745,0.746l0.51,0.509L14.869,17.64H23V18.36z"></path>
</svg>