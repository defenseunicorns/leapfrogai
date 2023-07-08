package util

// Int32 returns a pointer to the int32 value passed in.
func Int32(v int32) *int32 {
	return &v
}

// Int32Value returns the value of the int32 pointer passed in or
// 0 if the pointer is nil.
func Int32Value(v *int32) int32 {
	if v != nil {
		return *v
	}
	return 0
}

// Float32 returns a pointer to the float32 value passed in.
func Float32(v float32) *float32 {
	return &v
}

// Float32Value returns the value of the float32 pointer passed in or
// 0 if the pointer is nil.
func Float32Value(v *float32) float32 {
	if v != nil {
		return *v
	}
	return 0
}

// String returns a pointer to the string value passed in.
func String(v string) *string {
	return &v
}

// StringValue returns the value of the string pointer passed in or
// "" if the pointer is nil.
func StringValue(v *string) string {
	if v != nil {
		return *v
	}
	return ""
}

// Bool returns a pointer to the bool value passed in.
func Bool(v bool) *bool {
	return &v
}

// BoolValue returns the value of the bool pointer passed in or
// false if the pointer is nil.
func BoolValue(v *bool) bool {
	if v != nil {
		return *v
	}
	return false
}
