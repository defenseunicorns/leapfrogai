// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.28.1
// 	protoc        v4.23.3
// source: embeddings/embeddings.proto

package embeddings

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

// EmbeddingRequest is the payload to embedding creation
type EmbeddingRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Inputs []string `protobuf:"bytes,1,rep,name=inputs,proto3" json:"inputs,omitempty"`
}

func (x *EmbeddingRequest) Reset() {
	*x = EmbeddingRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_embeddings_embeddings_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *EmbeddingRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*EmbeddingRequest) ProtoMessage() {}

func (x *EmbeddingRequest) ProtoReflect() protoreflect.Message {
	mi := &file_embeddings_embeddings_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use EmbeddingRequest.ProtoReflect.Descriptor instead.
func (*EmbeddingRequest) Descriptor() ([]byte, []int) {
	return file_embeddings_embeddings_proto_rawDescGZIP(), []int{0}
}

func (x *EmbeddingRequest) GetInputs() []string {
	if x != nil {
		return x.Inputs
	}
	return nil
}

type Embedding struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Embedding []float32 `protobuf:"fixed32,1,rep,packed,name=embedding,proto3" json:"embedding,omitempty"`
}

func (x *Embedding) Reset() {
	*x = Embedding{}
	if protoimpl.UnsafeEnabled {
		mi := &file_embeddings_embeddings_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Embedding) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Embedding) ProtoMessage() {}

func (x *Embedding) ProtoReflect() protoreflect.Message {
	mi := &file_embeddings_embeddings_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Embedding.ProtoReflect.Descriptor instead.
func (*Embedding) Descriptor() ([]byte, []int) {
	return file_embeddings_embeddings_proto_rawDescGZIP(), []int{1}
}

func (x *Embedding) GetEmbedding() []float32 {
	if x != nil {
		return x.Embedding
	}
	return nil
}

// EmbeddingResponse are what's returned by the gRPC service
type EmbeddingResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Embeddings []*Embedding `protobuf:"bytes,1,rep,name=embeddings,proto3" json:"embeddings,omitempty"`
}

func (x *EmbeddingResponse) Reset() {
	*x = EmbeddingResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_embeddings_embeddings_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *EmbeddingResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*EmbeddingResponse) ProtoMessage() {}

func (x *EmbeddingResponse) ProtoReflect() protoreflect.Message {
	mi := &file_embeddings_embeddings_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use EmbeddingResponse.ProtoReflect.Descriptor instead.
func (*EmbeddingResponse) Descriptor() ([]byte, []int) {
	return file_embeddings_embeddings_proto_rawDescGZIP(), []int{2}
}

func (x *EmbeddingResponse) GetEmbeddings() []*Embedding {
	if x != nil {
		return x.Embeddings
	}
	return nil
}

var File_embeddings_embeddings_proto protoreflect.FileDescriptor

var file_embeddings_embeddings_proto_rawDesc = []byte{
	0x0a, 0x1b, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x73, 0x2f, 0x65, 0x6d, 0x62,
	0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x0a, 0x65,
	0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x73, 0x22, 0x2a, 0x0a, 0x10, 0x45, 0x6d, 0x62,
	0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x16, 0x0a,
	0x06, 0x69, 0x6e, 0x70, 0x75, 0x74, 0x73, 0x18, 0x01, 0x20, 0x03, 0x28, 0x09, 0x52, 0x06, 0x69,
	0x6e, 0x70, 0x75, 0x74, 0x73, 0x22, 0x29, 0x0a, 0x09, 0x45, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69,
	0x6e, 0x67, 0x12, 0x1c, 0x0a, 0x09, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x18,
	0x01, 0x20, 0x03, 0x28, 0x02, 0x52, 0x09, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67,
	0x22, 0x4a, 0x0a, 0x11, 0x45, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x52, 0x65, 0x73,
	0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x35, 0x0a, 0x0a, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69,
	0x6e, 0x67, 0x73, 0x18, 0x01, 0x20, 0x03, 0x28, 0x0b, 0x32, 0x15, 0x2e, 0x65, 0x6d, 0x62, 0x65,
	0x64, 0x64, 0x69, 0x6e, 0x67, 0x73, 0x2e, 0x45, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67,
	0x52, 0x0a, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x73, 0x32, 0x63, 0x0a, 0x11,
	0x45, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x73, 0x53, 0x65, 0x72, 0x76, 0x69, 0x63,
	0x65, 0x12, 0x4e, 0x0a, 0x0f, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x45, 0x6d, 0x62, 0x65, 0x64,
	0x64, 0x69, 0x6e, 0x67, 0x12, 0x1c, 0x2e, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67,
	0x73, 0x2e, 0x45, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x52, 0x65, 0x71, 0x75, 0x65,
	0x73, 0x74, 0x1a, 0x1d, 0x2e, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x73, 0x2e,
	0x45, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73,
	0x65, 0x42, 0x3d, 0x5a, 0x3b, 0x67, 0x69, 0x74, 0x68, 0x75, 0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f,
	0x64, 0x65, 0x66, 0x65, 0x6e, 0x73, 0x65, 0x75, 0x6e, 0x69, 0x63, 0x6f, 0x72, 0x6e, 0x73, 0x2f,
	0x6c, 0x65, 0x61, 0x70, 0x66, 0x72, 0x6f, 0x67, 0x61, 0x69, 0x2f, 0x70, 0x6b, 0x67, 0x2f, 0x63,
	0x6c, 0x69, 0x65, 0x6e, 0x74, 0x2f, 0x65, 0x6d, 0x62, 0x65, 0x64, 0x64, 0x69, 0x6e, 0x67, 0x73,
	0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_embeddings_embeddings_proto_rawDescOnce sync.Once
	file_embeddings_embeddings_proto_rawDescData = file_embeddings_embeddings_proto_rawDesc
)

func file_embeddings_embeddings_proto_rawDescGZIP() []byte {
	file_embeddings_embeddings_proto_rawDescOnce.Do(func() {
		file_embeddings_embeddings_proto_rawDescData = protoimpl.X.CompressGZIP(file_embeddings_embeddings_proto_rawDescData)
	})
	return file_embeddings_embeddings_proto_rawDescData
}

var file_embeddings_embeddings_proto_msgTypes = make([]protoimpl.MessageInfo, 3)
var file_embeddings_embeddings_proto_goTypes = []interface{}{
	(*EmbeddingRequest)(nil),  // 0: embeddings.EmbeddingRequest
	(*Embedding)(nil),         // 1: embeddings.Embedding
	(*EmbeddingResponse)(nil), // 2: embeddings.EmbeddingResponse
}
var file_embeddings_embeddings_proto_depIdxs = []int32{
	1, // 0: embeddings.EmbeddingResponse.embeddings:type_name -> embeddings.Embedding
	0, // 1: embeddings.EmbeddingsService.CreateEmbedding:input_type -> embeddings.EmbeddingRequest
	2, // 2: embeddings.EmbeddingsService.CreateEmbedding:output_type -> embeddings.EmbeddingResponse
	2, // [2:3] is the sub-list for method output_type
	1, // [1:2] is the sub-list for method input_type
	1, // [1:1] is the sub-list for extension type_name
	1, // [1:1] is the sub-list for extension extendee
	0, // [0:1] is the sub-list for field type_name
}

func init() { file_embeddings_embeddings_proto_init() }
func file_embeddings_embeddings_proto_init() {
	if File_embeddings_embeddings_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_embeddings_embeddings_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*EmbeddingRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_embeddings_embeddings_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Embedding); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_embeddings_embeddings_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*EmbeddingResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_embeddings_embeddings_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   3,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_embeddings_embeddings_proto_goTypes,
		DependencyIndexes: file_embeddings_embeddings_proto_depIdxs,
		MessageInfos:      file_embeddings_embeddings_proto_msgTypes,
	}.Build()
	File_embeddings_embeddings_proto = out.File
	file_embeddings_embeddings_proto_rawDesc = nil
	file_embeddings_embeddings_proto_goTypes = nil
	file_embeddings_embeddings_proto_depIdxs = nil
}
