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
  <path d="M16.36,31h-0.72v-2.64H1c-0.199,0-0.36-0.161-0.36-0.36v-4c0-0.199,0.161-0.36,0.36-0.36h14.64	v-2.28H4c-0.199,0-0.36-0.161-0.36-0.36v-4c0-0.199,0.161-0.36,0.36-0.36h11.64v-2.28H7c-0.199,0-0.36-0.161-0.36-0.36v-4	c0-0.199,0.161-0.36,0.36-0.36h8.64V7.36H10C9.801,7.36,9.64,7.199,9.64,7V3c0-0.199,0.161-0.36,0.36-0.36h5.64V1h0.72v1.64H22	c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36h-5.64v2.28H25c0.199,0,0.36,0.161,0.36,0.36v4	c0,0.199-0.161,0.36-0.36,0.36h-8.64v2.28H28c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36H16.36v2.279H31	c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36H16.36V31z M16.36,27.64h14.28v-3.28H16.36V27.64z M1.36,27.64h14.28	v-3.28H1.36V27.64z M16.36,20.64h11.28v-3.28H16.36V20.64z M4.36,20.64h11.28v-3.28H4.36V20.64z M16.36,13.64h8.28v-3.28h-8.28	V13.64z M7.36,13.64h8.28v-3.28H7.36V13.64z M16.36,6.64h5.28V3.36h-5.28V6.64z M10.36,6.64h5.28V3.36h-5.28	C10.36,3.36,10.36,6.64,10.36,6.64z"></path>
</svg>