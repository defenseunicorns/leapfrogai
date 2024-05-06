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
  <path d="M21,30.36H11c-2.404,0-4.36-1.956-4.36-4.36V10c0-2.404,1.956-4.36,4.36-4.36h0.655	c0.184-2.236,2.062-4,4.345-4s4.162,1.764,4.346,4H21c2.404,0,4.36,1.956,4.36,4.36v16C25.36,28.404,23.404,30.36,21,30.36z M11,6.36c-2.007,0-3.64,1.633-3.64,3.64v16c0,2.007,1.633,3.64,3.64,3.64h10c2.007,0,3.64-1.633,3.64-3.64V10	c0-2.007-1.633-3.64-3.64-3.64C21,6.36,11,6.36,11,6.36z M12.377,5.64h7.245C19.44,3.801,17.886,2.36,16,2.36	S12.559,3.801,12.377,5.64z M9.36,23H8.64v-2c0-0.199,0.161-0.36,0.36-0.36h14v0.721H9.36V23z M9.36,16H8.64v-2h0.72	C9.36,14,9.36,16,9.36,16z M23.36,15h-0.72v-5c0-0.904-0.735-1.64-1.64-1.64H11c-0.904,0-1.64,0.736-1.64,1.64v3H8.64v-3	c0-1.301,1.059-2.36,2.36-2.36h10c1.302,0,2.36,1.059,2.36,2.36V15z"></path>
</svg>