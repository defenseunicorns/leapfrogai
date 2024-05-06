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
  <path d="M16,31.36c-0.059,0-0.117-0.015-0.171-0.043l-13-7C2.713,24.254,2.64,24.133,2.64,24V8	c0-0.132,0.073-0.254,0.189-0.317l13-7c0.107-0.058,0.234-0.058,0.342,0l13,7C29.287,7.746,29.36,7.868,29.36,8v16	c0,0.133-0.073,0.254-0.189,0.317l-13,7C16.117,31.346,16.059,31.36,16,31.36z M3.36,23.785L16,30.591l12.64-6.806V8.215L16,1.409	L3.36,8.215V23.785z M23,22.36H13c-0.199,0-0.36-0.161-0.36-0.36v-2.64H9c-0.199,0-0.36-0.161-0.36-0.36v-9	c0-0.199,0.161-0.36,0.36-0.36h10c0.199,0,0.36,0.161,0.36,0.36v2.64H23c0.199,0,0.36,0.161,0.36,0.36v9	C23.36,22.199,23.199,22.36,23,22.36z M13.36,21.64h9.28v-8.28h-9.28V21.64z M9.36,18.64h3.28V13c0-0.199,0.161-0.36,0.36-0.36h5.64	v-2.28H9.36V18.64z"></path>
</svg>