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
  <path d="M31,31.36H1v-0.72h30V31.36z M31.36,24V1c0-0.199-0.161-0.36-0.36-0.36H1	C0.801,0.64,0.64,0.801,0.64,1v23c0,0.199,0.161,0.36,0.36,0.36h30C31.199,24.36,31.36,24.199,31.36,24z M1.36,1.36h29.28v22.28	H1.36V1.36z M8.003,17.167c1.624,0,2.815-0.854,3.432-2.228l-0.938-0.588c-0.393,1.064-1.247,1.765-2.493,1.765	c-1.682,0-2.676-1.219-2.676-3.222v-1.456c0-2.004,0.994-3.334,2.676-3.334c1.204,0,2.017,0.658,2.409,1.667l0.952-0.574	c-0.616-1.359-1.737-2.144-3.361-2.144c-2.466,0-3.937,1.849-3.937,5.112C4.066,15.431,5.537,17.167,8.003,17.167z M16.682,16.131	v-2.928h2.731V12.25h-2.731V9.323h-1.064v2.927h-2.731v0.953h2.731v2.928H16.682z M25.081,16.131v-2.928h2.731V12.25h-2.731V9.323	h-1.064v2.927h-2.731v0.953h2.731v2.928H25.081z"></path>
</svg>