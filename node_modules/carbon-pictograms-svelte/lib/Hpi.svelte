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
  <path d="M10,15.36H6c-0.199,0-0.36-0.161-0.36-0.36v-4.64H1c-0.199,0-0.36-0.161-0.36-0.36V6	c0-0.199,0.161-0.36,0.36-0.36h4.64V1c0-0.199,0.161-0.36,0.36-0.36h4c0.199,0,0.36,0.161,0.36,0.36v4.64H15	c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36h-4.64V15C10.36,15.199,10.199,15.36,10,15.36z M6.36,14.64h3.28V10	c0-0.199,0.161-0.36,0.36-0.36h4.64V6.36H10C9.801,6.36,9.64,6.199,9.64,6V1.36H6.36V6c0,0.199-0.161,0.36-0.36,0.36H1.36v3.28H6	c0.199,0,0.36,0.161,0.36,0.36V14.64z M29.36,31h-0.72V5.869l-1.385,1.385l-0.51-0.509L29,4.491l2.255,2.255l-0.51,0.509	L29.36,5.869V31z M24.36,31h-0.72V10.869l-1.385,1.385l-0.51-0.509L24,9.491l2.255,2.255l-0.51,0.509L24.36,10.87V31z M19.36,31	h-0.72V15.869l-1.385,1.386l-0.509-0.509L19,14.491l2.255,2.255l-0.51,0.509l-1.385-1.386V31z M14.36,31h-0.72V20.869l-1.386,1.386	l-0.509-0.51L14,19.491l2.254,2.254l-0.509,0.51l-1.386-1.386L14.36,31L14.36,31z M9.36,31H8.64v-5.131l-1.386,1.386l-0.509-0.51	L9,24.491l2.254,2.254l-0.509,0.51L9.36,25.869V31z"></path>
</svg>