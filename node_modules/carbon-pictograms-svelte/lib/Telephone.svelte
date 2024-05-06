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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V7c0-0.199,0.161-0.36,0.36-0.36h2.64V5	c0-1.301,1.059-2.36,2.36-2.36h4c1.301,0,2.36,1.059,2.36,2.36v1.64h16.28V1c0-0.199,0.161-0.36,0.36-0.36S29.36,0.801,29.36,1v5.64	H31c0.199,0,0.36,0.161,0.36,0.36v24C31.36,31.199,31.199,31.36,31,31.36z M1.36,30.64h29.28V7.36H12.36V27	c0,1.302-1.059,2.36-2.36,2.36H6c-1.301,0-2.36-1.059-2.36-2.36V7.36H1.36V30.64z M4.36,7v20c0,0.904,0.736,1.64,1.64,1.64h4	c0.904,0,1.64-0.735,1.64-1.64V5c0-0.904-0.736-1.64-1.64-1.64H6C5.096,3.36,4.36,4.096,4.36,5V7z M28,23.36h-6	c-0.199,0-0.36-0.161-0.36-0.36s0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36S28.199,23.36,28,23.36z M28,20.36H15	c-0.199,0-0.36-0.161-0.36-0.36V10c0-0.199,0.161-0.36,0.36-0.36h13c0.199,0,0.36,0.161,0.36,0.36v10	C28.36,20.199,28.199,20.36,28,20.36z M15.36,19.64h12.28v-9.28H15.36V19.64z"></path>
</svg>