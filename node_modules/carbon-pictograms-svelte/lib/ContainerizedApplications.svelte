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
  <path d="M16,31.36	c-0.059,0-0.117-0.015-0.171-0.043l-13-7C2.713,24.254,2.64,24.133,2.64,24V8c0-0.132,0.073-0.254,0.189-0.317l13-7	c0.107-0.058,0.234-0.058,0.342,0l13,7C29.287,7.746,29.36,7.868,29.36,8v16c0,0.133-0.073,0.254-0.189,0.317l-13,7	C16.117,31.346,16.059,31.36,16,31.36z M3.36,23.785L16,30.591l12.64-6.806V8.215L16,1.409L3.36,8.215V23.785z M23,23.36H13	c-0.199,0-0.36-0.161-0.36-0.36v-3.64H9c-0.199,0-0.36-0.161-0.36-0.36v-9c0-0.199,0.161-0.36,0.36-0.36h10	c0.199,0,0.36,0.161,0.36,0.36v3.64H23c0.199,0,0.36,0.161,0.36,0.36v9C23.36,23.199,23.199,23.36,23,23.36z M13.36,22.64h9.28	v-8.28h-9.28V22.64z M9.36,18.64h3.28V14c0-0.199,0.161-0.36,0.36-0.36h5.64v-3.28H9.36V18.64z M17,16.36h-2v-0.72h2V16.36z M13,12.36h-2v-0.72h2V12.36z"></path>
</svg>