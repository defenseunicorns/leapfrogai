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
  <path d="M3.746,27.745L5.491,26l-1.745-1.745l0.509-0.51L6,25.491l1.746-1.746l0.509,0.51L6.509,26	l1.745,1.745l-0.509,0.51L6,26.509l-1.746,1.746L3.746,27.745z M31.36,1v20c0,0.199-0.161,0.36-0.36,0.36H11.36V31	c0,0.199-0.161,0.36-0.36,0.36H1c-0.199,0-0.36-0.161-0.36-0.36V21c0-0.199,0.161-0.36,0.36-0.36h9.64V1	c0-0.199,0.161-0.36,0.36-0.36h20C31.199,0.64,31.36,0.801,31.36,1z M10.64,21.36H1.36v9.279h9.28	C10.64,30.639,10.64,21.36,10.64,21.36z M30.64,1.36H11.36v19.28h19.28V1.36z M17.255,15.254L21,11.509l3.745,3.745l0.51-0.509	L21.509,11l3.746-3.746l-0.51-0.509L21,10.491l-3.745-3.745l-0.509,0.509L20.491,11l-3.745,3.746L17.255,15.254z"></path>
</svg>