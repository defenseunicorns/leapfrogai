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
  <path d="M26,31.36H6c-0.16,0-0.3-0.105-0.345-0.259l-5-17c-0.04-0.135,0.003-0.281,0.109-0.374l15-13	c0.136-0.117,0.336-0.117,0.472,0l15,13c0.107,0.092,0.149,0.238,0.11,0.374l-5,17C26.301,31.255,26.16,31.36,26,31.36z M6.731,30.64h18.538l-5.514-7.168L9.328,27.264L6.731,30.64z M20.379,23.103l5.476,7.117l4.619-15.707l-4.133,1.102	c-0.013,0.039-0.033,0.076-0.06,0.11L20.379,23.103z M1.526,14.513l4.62,15.707l2.494-3.242V16.41L1.526,14.513z M16,18.591	L10.146,26.2l9.148-3.327L16,18.591z M9.36,16.602v9.44l6.025-7.833L9.36,16.602z M16.615,18.209l3.312,4.306l5.277-6.597	L16.615,18.209z M16.36,5.9v11.631l8.834-2.355L16.36,5.9z M9.495,15.893l6.145,1.639V6.236L9.495,15.893z M1.749,13.827	l7.016,1.871L15.64,4.895V1.789L1.749,13.827z M16.36,4.856l9.627,10.108l4.264-1.137L16.36,1.789V4.856z"></path>
</svg>