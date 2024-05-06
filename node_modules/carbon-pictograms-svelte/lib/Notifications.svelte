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
  <path d="M31,28.86c-0.094,0-0.186-0.037-0.255-0.105	L25.35,23.36H3c-1.301,0-2.36-1.059-2.36-2.36V5c0-1.301,1.059-2.36,2.36-2.36h26c1.302,0,2.36,1.059,2.36,2.36v23.5	c0,0.146-0.088,0.277-0.223,0.333C31.093,28.851,31.047,28.86,31,28.86z M3,3.36C2.096,3.36,1.36,4.096,1.36,5v16	c0,0.904,0.736,1.64,1.64,1.64h22.5c0.096,0,0.188,0.038,0.255,0.105l4.885,4.886V5c0-0.904-0.735-1.64-1.64-1.64	C29,3.36,3,3.36,3,3.36z M25,17.36H7v-0.72h18V17.36z M25,13.36H7v-0.72h18V13.36z M25,9.36H7V8.64h18V9.36z"></path>
</svg>