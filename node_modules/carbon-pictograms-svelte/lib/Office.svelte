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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h18c0.199,0,0.36,0.161,0.36,0.36	v2.64H25c0.199,0,0.36,0.161,0.36,0.36v3.64H31c0.199,0,0.36,0.161,0.36,0.36v23C31.36,31.199,31.199,31.36,31,31.36z M19.36,30.64	h11.28V8.36H19.36V30.64z M12.36,30.64h6.28V1.36H1.36v29.28h6.28V23c0-0.199,0.161-0.36,0.36-0.36h4c0.199,0,0.36,0.161,0.36,0.36	V30.64z M8.36,30.64h3.28v-7.28H8.36V30.64z M19.36,7.64h5.279V4.36H19.36V7.64z M27.36,25h-0.72v-2h0.721L27.36,25L27.36,25z M23.36,25h-0.72v-2h0.721L23.36,25L23.36,25z M16.36,25h-0.72v-2h0.72V25z M4.36,25H3.64v-2h0.72V25z M27.36,19h-0.72v-2h0.721	L27.36,19L27.36,19z M23.36,19h-0.72v-2h0.721L23.36,19L23.36,19z M16.36,19h-0.72v-2h0.72V19z M12.36,19h-0.72v-2h0.72V19z M8.36,19H7.64v-2h0.72V19z M4.36,19H3.64v-2h0.72V19z M27.36,13h-0.72v-2h0.721L27.36,13L27.36,13z M23.36,13h-0.72v-2h0.721	L23.36,13L23.36,13z M16.36,13h-0.72v-2h0.72V13z M12.36,13h-0.72v-2h0.72V13z M8.36,13H7.64v-2h0.72V13z M4.36,13H3.64v-2h0.72V13z M16.36,7h-0.72V5h0.72V7z M12.36,7h-0.72V5h0.72V7z M8.36,7H7.64V5h0.72V7z M4.36,7H3.64V5h0.72V7z"></path>
</svg>