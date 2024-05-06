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
  <path d="M31,31.36H1v-0.72h30V31.36z M31.36,24V1c0-0.199-0.161-0.36-0.36-0.36H1 C0.801,0.64,0.64,0.801,0.64,1v23c0,0.199,0.161,0.36,0.36,0.36h30C31.199,24.36,31.36,24.199,31.36,24z M1.36,1.36h29.28v22.28 H1.36V1.36z M16.402,17.169c1.624,0,2.815-0.854,3.432-2.228l-0.939-0.588c-0.393,1.064-1.246,1.765-2.493,1.765 c-1.682,0-2.676-1.219-2.676-3.222V11.44c0-2.004,0.994-3.334,2.676-3.334c1.204,0,2.016,0.658,2.409,1.667l0.953-0.574 c-0.617-1.359-1.738-2.144-3.362-2.144c-2.466,0-3.937,1.849-3.937,5.112C12.465,15.433,13.936,17.169,16.402,17.169z"></path>
</svg>