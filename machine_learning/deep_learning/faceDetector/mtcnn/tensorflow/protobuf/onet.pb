
M
input_imagePlaceholder*
dtype0*$
shape:?????????00
?
.conv1/weights/Initializer/random_uniform/shapeConst*%
valueB"             *
dtype0* 
_class
loc:@conv1/weights
{
,conv1/weights/Initializer/random_uniform/minConst*
valueB
 *OS?*
dtype0* 
_class
loc:@conv1/weights
{
,conv1/weights/Initializer/random_uniform/maxConst*
valueB
 *OS>*
dtype0* 
_class
loc:@conv1/weights
?
6conv1/weights/Initializer/random_uniform/RandomUniformRandomUniform.conv1/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed * 
_class
loc:@conv1/weights
?
,conv1/weights/Initializer/random_uniform/subSub,conv1/weights/Initializer/random_uniform/max,conv1/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv1/weights
?
,conv1/weights/Initializer/random_uniform/mulMul6conv1/weights/Initializer/random_uniform/RandomUniform,conv1/weights/Initializer/random_uniform/sub*
T0* 
_class
loc:@conv1/weights
?
(conv1/weights/Initializer/random_uniformAdd,conv1/weights/Initializer/random_uniform/mul,conv1/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv1/weights
?
conv1/weights
VariableV2*
dtype0*
shared_name *
	container *
shape: * 
_class
loc:@conv1/weights
?
conv1/weights/AssignAssignconv1/weights(conv1/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv1/weights
X
conv1/weights/readIdentityconv1/weights*
T0* 
_class
loc:@conv1/weights
|
-conv1/kernel/Regularizer/l2_regularizer/scaleConst*
valueB
 *o:*
dtype0* 
_class
loc:@conv1/weights
w
.conv1/kernel/Regularizer/l2_regularizer/L2LossL2Lossconv1/weights/read*
T0* 
_class
loc:@conv1/weights
?
'conv1/kernel/Regularizer/l2_regularizerMul-conv1/kernel/Regularizer/l2_regularizer/scale.conv1/kernel/Regularizer/l2_regularizer/L2Loss*
T0* 
_class
loc:@conv1/weights
p
conv1/biases/Initializer/zerosConst*
valueB *    *
dtype0*
_class
loc:@conv1/biases
}
conv1/biases
VariableV2*
dtype0*
shared_name *
	container *
shape: *
_class
loc:@conv1/biases
?
conv1/biases/AssignAssignconv1/biasesconv1/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv1/biases
U
conv1/biases/readIdentityconv1/biases*
T0*
_class
loc:@conv1/biases
H
conv1/dilation_rateConst*
valueB"      *
dtype0
?
conv1/Conv2DConv2Dinput_imageconv1/weights/read*
strides
*
	dilations
*
T0*
data_formatNHWC*
paddingVALID*
use_cudnn_on_gpu(
Y
conv1/BiasAddBiasAddconv1/Conv2Dconv1/biases/read*
T0*
data_formatNHWC
p
conv1/alphas/Initializer/ConstConst*
valueB *  ?>*
dtype0*
_class
loc:@conv1/alphas
}
conv1/alphas
VariableV2*
dtype0*
shared_name *
	container *
shape: *
_class
loc:@conv1/alphas
?
conv1/alphas/AssignAssignconv1/alphasconv1/alphas/Initializer/Const*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv1/alphas
U
conv1/alphas/readIdentityconv1/alphas*
T0*
_class
loc:@conv1/alphas
*

conv1/ReluReluconv1/BiasAdd*
T0
(
	conv1/AbsAbsconv1/BiasAdd*
T0
3
	conv1/subSubconv1/BiasAdd	conv1/Abs*
T0
7
	conv1/mulMulconv1/alphas/read	conv1/sub*
T0
:
conv1/mul_1/yConst*
valueB
 *   ?*
dtype0
5
conv1/mul_1Mul	conv1/mulconv1/mul_1/y*
T0
2
	conv1/addAdd
conv1/Reluconv1/mul_1*
T0
~
pool1/MaxPoolMaxPool	conv1/add*
T0*
strides
*
data_formatNHWC*
paddingSAME*
ksize

?
.conv2/weights/Initializer/random_uniform/shapeConst*%
valueB"          @   *
dtype0* 
_class
loc:@conv2/weights
{
,conv2/weights/Initializer/random_uniform/minConst*
valueB
 *????*
dtype0* 
_class
loc:@conv2/weights
{
,conv2/weights/Initializer/random_uniform/maxConst*
valueB
 *???=*
dtype0* 
_class
loc:@conv2/weights
?
6conv2/weights/Initializer/random_uniform/RandomUniformRandomUniform.conv2/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed * 
_class
loc:@conv2/weights
?
,conv2/weights/Initializer/random_uniform/subSub,conv2/weights/Initializer/random_uniform/max,conv2/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv2/weights
?
,conv2/weights/Initializer/random_uniform/mulMul6conv2/weights/Initializer/random_uniform/RandomUniform,conv2/weights/Initializer/random_uniform/sub*
T0* 
_class
loc:@conv2/weights
?
(conv2/weights/Initializer/random_uniformAdd,conv2/weights/Initializer/random_uniform/mul,conv2/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv2/weights
?
conv2/weights
VariableV2*
dtype0*
shared_name *
	container *
shape: @* 
_class
loc:@conv2/weights
?
conv2/weights/AssignAssignconv2/weights(conv2/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv2/weights
X
conv2/weights/readIdentityconv2/weights*
T0* 
_class
loc:@conv2/weights
|
-conv2/kernel/Regularizer/l2_regularizer/scaleConst*
valueB
 *o:*
dtype0* 
_class
loc:@conv2/weights
w
.conv2/kernel/Regularizer/l2_regularizer/L2LossL2Lossconv2/weights/read*
T0* 
_class
loc:@conv2/weights
?
'conv2/kernel/Regularizer/l2_regularizerMul-conv2/kernel/Regularizer/l2_regularizer/scale.conv2/kernel/Regularizer/l2_regularizer/L2Loss*
T0* 
_class
loc:@conv2/weights
p
conv2/biases/Initializer/zerosConst*
valueB@*    *
dtype0*
_class
loc:@conv2/biases
}
conv2/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:@*
_class
loc:@conv2/biases
?
conv2/biases/AssignAssignconv2/biasesconv2/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv2/biases
U
conv2/biases/readIdentityconv2/biases*
T0*
_class
loc:@conv2/biases
H
conv2/dilation_rateConst*
valueB"      *
dtype0
?
conv2/Conv2DConv2Dpool1/MaxPoolconv2/weights/read*
strides
*
	dilations
*
T0*
data_formatNHWC*
paddingVALID*
use_cudnn_on_gpu(
Y
conv2/BiasAddBiasAddconv2/Conv2Dconv2/biases/read*
T0*
data_formatNHWC
p
conv2/alphas/Initializer/ConstConst*
valueB@*  ?>*
dtype0*
_class
loc:@conv2/alphas
}
conv2/alphas
VariableV2*
dtype0*
shared_name *
	container *
shape:@*
_class
loc:@conv2/alphas
?
conv2/alphas/AssignAssignconv2/alphasconv2/alphas/Initializer/Const*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv2/alphas
U
conv2/alphas/readIdentityconv2/alphas*
T0*
_class
loc:@conv2/alphas
*

conv2/ReluReluconv2/BiasAdd*
T0
(
	conv2/AbsAbsconv2/BiasAdd*
T0
3
	conv2/subSubconv2/BiasAdd	conv2/Abs*
T0
7
	conv2/mulMulconv2/alphas/read	conv2/sub*
T0
:
conv2/mul_1/yConst*
valueB
 *   ?*
dtype0
5
conv2/mul_1Mul	conv2/mulconv2/mul_1/y*
T0
2
	conv2/addAdd
conv2/Reluconv2/mul_1*
T0

pool2/MaxPoolMaxPool	conv2/add*
T0*
strides
*
data_formatNHWC*
paddingVALID*
ksize

?
.conv3/weights/Initializer/random_uniform/shapeConst*%
valueB"      @   @   *
dtype0* 
_class
loc:@conv3/weights
{
,conv3/weights/Initializer/random_uniform/minConst*
valueB
 *:͓?*
dtype0* 
_class
loc:@conv3/weights
{
,conv3/weights/Initializer/random_uniform/maxConst*
valueB
 *:͓=*
dtype0* 
_class
loc:@conv3/weights
?
6conv3/weights/Initializer/random_uniform/RandomUniformRandomUniform.conv3/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed * 
_class
loc:@conv3/weights
?
,conv3/weights/Initializer/random_uniform/subSub,conv3/weights/Initializer/random_uniform/max,conv3/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv3/weights
?
,conv3/weights/Initializer/random_uniform/mulMul6conv3/weights/Initializer/random_uniform/RandomUniform,conv3/weights/Initializer/random_uniform/sub*
T0* 
_class
loc:@conv3/weights
?
(conv3/weights/Initializer/random_uniformAdd,conv3/weights/Initializer/random_uniform/mul,conv3/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv3/weights
?
conv3/weights
VariableV2*
dtype0*
shared_name *
	container *
shape:@@* 
_class
loc:@conv3/weights
?
conv3/weights/AssignAssignconv3/weights(conv3/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv3/weights
X
conv3/weights/readIdentityconv3/weights*
T0* 
_class
loc:@conv3/weights
|
-conv3/kernel/Regularizer/l2_regularizer/scaleConst*
valueB
 *o:*
dtype0* 
_class
loc:@conv3/weights
w
.conv3/kernel/Regularizer/l2_regularizer/L2LossL2Lossconv3/weights/read*
T0* 
_class
loc:@conv3/weights
?
'conv3/kernel/Regularizer/l2_regularizerMul-conv3/kernel/Regularizer/l2_regularizer/scale.conv3/kernel/Regularizer/l2_regularizer/L2Loss*
T0* 
_class
loc:@conv3/weights
p
conv3/biases/Initializer/zerosConst*
valueB@*    *
dtype0*
_class
loc:@conv3/biases
}
conv3/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:@*
_class
loc:@conv3/biases
?
conv3/biases/AssignAssignconv3/biasesconv3/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv3/biases
U
conv3/biases/readIdentityconv3/biases*
T0*
_class
loc:@conv3/biases
H
conv3/dilation_rateConst*
valueB"      *
dtype0
?
conv3/Conv2DConv2Dpool2/MaxPoolconv3/weights/read*
strides
*
	dilations
*
T0*
data_formatNHWC*
paddingVALID*
use_cudnn_on_gpu(
Y
conv3/BiasAddBiasAddconv3/Conv2Dconv3/biases/read*
T0*
data_formatNHWC
p
conv3/alphas/Initializer/ConstConst*
valueB@*  ?>*
dtype0*
_class
loc:@conv3/alphas
}
conv3/alphas
VariableV2*
dtype0*
shared_name *
	container *
shape:@*
_class
loc:@conv3/alphas
?
conv3/alphas/AssignAssignconv3/alphasconv3/alphas/Initializer/Const*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv3/alphas
U
conv3/alphas/readIdentityconv3/alphas*
T0*
_class
loc:@conv3/alphas
*

conv3/ReluReluconv3/BiasAdd*
T0
(
	conv3/AbsAbsconv3/BiasAdd*
T0
3
	conv3/subSubconv3/BiasAdd	conv3/Abs*
T0
7
	conv3/mulMulconv3/alphas/read	conv3/sub*
T0
:
conv3/mul_1/yConst*
valueB
 *   ?*
dtype0
5
conv3/mul_1Mul	conv3/mulconv3/mul_1/y*
T0
2
	conv3/addAdd
conv3/Reluconv3/mul_1*
T0
~
pool3/MaxPoolMaxPool	conv3/add*
T0*
strides
*
data_formatNHWC*
paddingSAME*
ksize

?
.conv4/weights/Initializer/random_uniform/shapeConst*%
valueB"      @   ?   *
dtype0* 
_class
loc:@conv4/weights
{
,conv4/weights/Initializer/random_uniform/minConst*
valueB
 *???*
dtype0* 
_class
loc:@conv4/weights
{
,conv4/weights/Initializer/random_uniform/maxConst*
valueB
 *??=*
dtype0* 
_class
loc:@conv4/weights
?
6conv4/weights/Initializer/random_uniform/RandomUniformRandomUniform.conv4/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed * 
_class
loc:@conv4/weights
?
,conv4/weights/Initializer/random_uniform/subSub,conv4/weights/Initializer/random_uniform/max,conv4/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv4/weights
?
,conv4/weights/Initializer/random_uniform/mulMul6conv4/weights/Initializer/random_uniform/RandomUniform,conv4/weights/Initializer/random_uniform/sub*
T0* 
_class
loc:@conv4/weights
?
(conv4/weights/Initializer/random_uniformAdd,conv4/weights/Initializer/random_uniform/mul,conv4/weights/Initializer/random_uniform/min*
T0* 
_class
loc:@conv4/weights
?
conv4/weights
VariableV2*
dtype0*
shared_name *
	container *
shape:@?* 
_class
loc:@conv4/weights
?
conv4/weights/AssignAssignconv4/weights(conv4/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv4/weights
X
conv4/weights/readIdentityconv4/weights*
T0* 
_class
loc:@conv4/weights
|
-conv4/kernel/Regularizer/l2_regularizer/scaleConst*
valueB
 *o:*
dtype0* 
_class
loc:@conv4/weights
w
.conv4/kernel/Regularizer/l2_regularizer/L2LossL2Lossconv4/weights/read*
T0* 
_class
loc:@conv4/weights
?
'conv4/kernel/Regularizer/l2_regularizerMul-conv4/kernel/Regularizer/l2_regularizer/scale.conv4/kernel/Regularizer/l2_regularizer/L2Loss*
T0* 
_class
loc:@conv4/weights
q
conv4/biases/Initializer/zerosConst*
valueB?*    *
dtype0*
_class
loc:@conv4/biases
~
conv4/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:?*
_class
loc:@conv4/biases
?
conv4/biases/AssignAssignconv4/biasesconv4/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv4/biases
U
conv4/biases/readIdentityconv4/biases*
T0*
_class
loc:@conv4/biases
H
conv4/dilation_rateConst*
valueB"      *
dtype0
?
conv4/Conv2DConv2Dpool3/MaxPoolconv4/weights/read*
strides
*
	dilations
*
T0*
data_formatNHWC*
paddingVALID*
use_cudnn_on_gpu(
Y
conv4/BiasAddBiasAddconv4/Conv2Dconv4/biases/read*
T0*
data_formatNHWC
q
conv4/alphas/Initializer/ConstConst*
valueB?*  ?>*
dtype0*
_class
loc:@conv4/alphas
~
conv4/alphas
VariableV2*
dtype0*
shared_name *
	container *
shape:?*
_class
loc:@conv4/alphas
?
conv4/alphas/AssignAssignconv4/alphasconv4/alphas/Initializer/Const*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv4/alphas
U
conv4/alphas/readIdentityconv4/alphas*
T0*
_class
loc:@conv4/alphas
*

conv4/ReluReluconv4/BiasAdd*
T0
(
	conv4/AbsAbsconv4/BiasAdd*
T0
3
	conv4/subSubconv4/BiasAdd	conv4/Abs*
T0
7
	conv4/mulMulconv4/alphas/read	conv4/sub*
T0
:
conv4/mul_1/yConst*
valueB
 *   ?*
dtype0
5
conv4/mul_1Mul	conv4/mulconv4/mul_1/y*
T0
2
	conv4/addAdd
conv4/Reluconv4/mul_1*
T0
B
Flatten/flatten/ShapeShape	conv4/add*
T0*
out_type0
Q
#Flatten/flatten/strided_slice/stackConst*
valueB: *
dtype0
S
%Flatten/flatten/strided_slice/stack_1Const*
valueB:*
dtype0
S
%Flatten/flatten/strided_slice/stack_2Const*
valueB:*
dtype0
?
Flatten/flatten/strided_sliceStridedSliceFlatten/flatten/Shape#Flatten/flatten/strided_slice/stack%Flatten/flatten/strided_slice/stack_1%Flatten/flatten/strided_slice/stack_2*
Index0*
end_mask *
T0*
shrink_axis_mask*
new_axis_mask *

begin_mask *
ellipsis_mask 
R
Flatten/flatten/Reshape/shape/1Const*
valueB :
?????????*
dtype0
?
Flatten/flatten/Reshape/shapePackFlatten/flatten/strided_sliceFlatten/flatten/Reshape/shape/1*

axis *
T0*
N
c
Flatten/flatten/ReshapeReshape	conv4/addFlatten/flatten/Reshape/shape*
T0*
Tshape0
?
,fc1/weights/Initializer/random_uniform/shapeConst*
valueB"?     *
dtype0*
_class
loc:@fc1/weights
w
*fc1/weights/Initializer/random_uniform/minConst*
valueB
 *???*
dtype0*
_class
loc:@fc1/weights
w
*fc1/weights/Initializer/random_uniform/maxConst*
valueB
 *??=*
dtype0*
_class
loc:@fc1/weights
?
4fc1/weights/Initializer/random_uniform/RandomUniformRandomUniform,fc1/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed *
_class
loc:@fc1/weights
?
*fc1/weights/Initializer/random_uniform/subSub*fc1/weights/Initializer/random_uniform/max*fc1/weights/Initializer/random_uniform/min*
T0*
_class
loc:@fc1/weights
?
*fc1/weights/Initializer/random_uniform/mulMul4fc1/weights/Initializer/random_uniform/RandomUniform*fc1/weights/Initializer/random_uniform/sub*
T0*
_class
loc:@fc1/weights
?
&fc1/weights/Initializer/random_uniformAdd*fc1/weights/Initializer/random_uniform/mul*fc1/weights/Initializer/random_uniform/min*
T0*
_class
loc:@fc1/weights
?
fc1/weights
VariableV2*
dtype0*
shared_name *
	container *
shape:
?	?*
_class
loc:@fc1/weights
?
fc1/weights/AssignAssignfc1/weights&fc1/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(*
_class
loc:@fc1/weights
R
fc1/weights/readIdentityfc1/weights*
T0*
_class
loc:@fc1/weights
m
fc1/biases/Initializer/zerosConst*
valueB?*    *
dtype0*
_class
loc:@fc1/biases
z

fc1/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:?*
_class
loc:@fc1/biases
?
fc1/biases/AssignAssign
fc1/biasesfc1/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*
_class
loc:@fc1/biases
O
fc1/biases/readIdentity
fc1/biases*
T0*
_class
loc:@fc1/biases
n

fc1/MatMulMatMulFlatten/flatten/Reshapefc1/weights/read*
T0*
transpose_b( *
transpose_a( 
S
fc1/BiasAddBiasAdd
fc1/MatMulfc1/biases/read*
T0*
data_formatNHWC
&
fc1/ReluRelufc1/BiasAdd*
T0
?
/cls_fc/weights/Initializer/random_uniform/shapeConst*
valueB"      *
dtype0*!
_class
loc:@cls_fc/weights
}
-cls_fc/weights/Initializer/random_uniform/minConst*
valueB
 *?(?*
dtype0*!
_class
loc:@cls_fc/weights
}
-cls_fc/weights/Initializer/random_uniform/maxConst*
valueB
 *?(>*
dtype0*!
_class
loc:@cls_fc/weights
?
7cls_fc/weights/Initializer/random_uniform/RandomUniformRandomUniform/cls_fc/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed *!
_class
loc:@cls_fc/weights
?
-cls_fc/weights/Initializer/random_uniform/subSub-cls_fc/weights/Initializer/random_uniform/max-cls_fc/weights/Initializer/random_uniform/min*
T0*!
_class
loc:@cls_fc/weights
?
-cls_fc/weights/Initializer/random_uniform/mulMul7cls_fc/weights/Initializer/random_uniform/RandomUniform-cls_fc/weights/Initializer/random_uniform/sub*
T0*!
_class
loc:@cls_fc/weights
?
)cls_fc/weights/Initializer/random_uniformAdd-cls_fc/weights/Initializer/random_uniform/mul-cls_fc/weights/Initializer/random_uniform/min*
T0*!
_class
loc:@cls_fc/weights
?
cls_fc/weights
VariableV2*
dtype0*
shared_name *
	container *
shape:	?*!
_class
loc:@cls_fc/weights
?
cls_fc/weights/AssignAssigncls_fc/weights)cls_fc/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(*!
_class
loc:@cls_fc/weights
[
cls_fc/weights/readIdentitycls_fc/weights*
T0*!
_class
loc:@cls_fc/weights
r
cls_fc/biases/Initializer/zerosConst*
valueB*    *
dtype0* 
_class
loc:@cls_fc/biases

cls_fc/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:* 
_class
loc:@cls_fc/biases
?
cls_fc/biases/AssignAssigncls_fc/biasescls_fc/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(* 
_class
loc:@cls_fc/biases
X
cls_fc/biases/readIdentitycls_fc/biases*
T0* 
_class
loc:@cls_fc/biases
e
cls_fc/MatMulMatMulfc1/Relucls_fc/weights/read*
T0*
transpose_b( *
transpose_a( 
\
cls_fc/BiasAddBiasAddcls_fc/MatMulcls_fc/biases/read*
T0*
data_formatNHWC
2
cls_fc/SoftmaxSoftmaxcls_fc/BiasAdd*
T0
?
0bbox_fc/weights/Initializer/random_uniform/shapeConst*
valueB"      *
dtype0*"
_class
loc:@bbox_fc/weights

.bbox_fc/weights/Initializer/random_uniform/minConst*
valueB
 *???*
dtype0*"
_class
loc:@bbox_fc/weights

.bbox_fc/weights/Initializer/random_uniform/maxConst*
valueB
 *??>*
dtype0*"
_class
loc:@bbox_fc/weights
?
8bbox_fc/weights/Initializer/random_uniform/RandomUniformRandomUniform0bbox_fc/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed *"
_class
loc:@bbox_fc/weights
?
.bbox_fc/weights/Initializer/random_uniform/subSub.bbox_fc/weights/Initializer/random_uniform/max.bbox_fc/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@bbox_fc/weights
?
.bbox_fc/weights/Initializer/random_uniform/mulMul8bbox_fc/weights/Initializer/random_uniform/RandomUniform.bbox_fc/weights/Initializer/random_uniform/sub*
T0*"
_class
loc:@bbox_fc/weights
?
*bbox_fc/weights/Initializer/random_uniformAdd.bbox_fc/weights/Initializer/random_uniform/mul.bbox_fc/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@bbox_fc/weights
?
bbox_fc/weights
VariableV2*
dtype0*
shared_name *
	container *
shape:	?*"
_class
loc:@bbox_fc/weights
?
bbox_fc/weights/AssignAssignbbox_fc/weights*bbox_fc/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(*"
_class
loc:@bbox_fc/weights
^
bbox_fc/weights/readIdentitybbox_fc/weights*
T0*"
_class
loc:@bbox_fc/weights
t
 bbox_fc/biases/Initializer/zerosConst*
valueB*    *
dtype0*!
_class
loc:@bbox_fc/biases
?
bbox_fc/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:*!
_class
loc:@bbox_fc/biases
?
bbox_fc/biases/AssignAssignbbox_fc/biases bbox_fc/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*!
_class
loc:@bbox_fc/biases
[
bbox_fc/biases/readIdentitybbox_fc/biases*
T0*!
_class
loc:@bbox_fc/biases
g
bbox_fc/MatMulMatMulfc1/Relubbox_fc/weights/read*
T0*
transpose_b( *
transpose_a( 
_
bbox_fc/BiasAddBiasAddbbox_fc/MatMulbbox_fc/biases/read*
T0*
data_formatNHWC
?
4landmark_fc/weights/Initializer/random_uniform/shapeConst*
valueB"   
   *
dtype0*&
_class
loc:@landmark_fc/weights
?
2landmark_fc/weights/Initializer/random_uniform/minConst*
valueB
 *???*
dtype0*&
_class
loc:@landmark_fc/weights
?
2landmark_fc/weights/Initializer/random_uniform/maxConst*
valueB
 *??>*
dtype0*&
_class
loc:@landmark_fc/weights
?
<landmark_fc/weights/Initializer/random_uniform/RandomUniformRandomUniform4landmark_fc/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed *&
_class
loc:@landmark_fc/weights
?
2landmark_fc/weights/Initializer/random_uniform/subSub2landmark_fc/weights/Initializer/random_uniform/max2landmark_fc/weights/Initializer/random_uniform/min*
T0*&
_class
loc:@landmark_fc/weights
?
2landmark_fc/weights/Initializer/random_uniform/mulMul<landmark_fc/weights/Initializer/random_uniform/RandomUniform2landmark_fc/weights/Initializer/random_uniform/sub*
T0*&
_class
loc:@landmark_fc/weights
?
.landmark_fc/weights/Initializer/random_uniformAdd2landmark_fc/weights/Initializer/random_uniform/mul2landmark_fc/weights/Initializer/random_uniform/min*
T0*&
_class
loc:@landmark_fc/weights
?
landmark_fc/weights
VariableV2*
dtype0*
shared_name *
	container *
shape:	?
*&
_class
loc:@landmark_fc/weights
?
landmark_fc/weights/AssignAssignlandmark_fc/weights.landmark_fc/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(*&
_class
loc:@landmark_fc/weights
j
landmark_fc/weights/readIdentitylandmark_fc/weights*
T0*&
_class
loc:@landmark_fc/weights
|
$landmark_fc/biases/Initializer/zerosConst*
valueB
*    *
dtype0*%
_class
loc:@landmark_fc/biases
?
landmark_fc/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:
*%
_class
loc:@landmark_fc/biases
?
landmark_fc/biases/AssignAssignlandmark_fc/biases$landmark_fc/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*%
_class
loc:@landmark_fc/biases
g
landmark_fc/biases/readIdentitylandmark_fc/biases*
T0*%
_class
loc:@landmark_fc/biases
o
landmark_fc/MatMulMatMulfc1/Relulandmark_fc/weights/read*
T0*
transpose_b( *
transpose_a( 
k
landmark_fc/BiasAddBiasAddlandmark_fc/MatMullandmark_fc/biases/read*
T0*
data_formatNHWC
8

save/ConstConst*
valueB Bmodel*
dtype0
?
save/SaveV2/tensor_namesConst*?
value?B?Bbbox_fc/biasesBbbox_fc/weightsBcls_fc/biasesBcls_fc/weightsBconv1/alphasBconv1/biasesBconv1/weightsBconv2/alphasBconv2/biasesBconv2/weightsBconv3/alphasBconv3/biasesBconv3/weightsBconv4/alphasBconv4/biasesBconv4/weightsB
fc1/biasesBfc1/weightsBlandmark_fc/biasesBlandmark_fc/weights*
dtype0
o
save/SaveV2/shape_and_slicesConst*;
value2B0B B B B B B B B B B B B B B B B B B B B *
dtype0
?
save/SaveV2SaveV2
save/Constsave/SaveV2/tensor_namessave/SaveV2/shape_and_slicesbbox_fc/biasesbbox_fc/weightscls_fc/biasescls_fc/weightsconv1/alphasconv1/biasesconv1/weightsconv2/alphasconv2/biasesconv2/weightsconv3/alphasconv3/biasesconv3/weightsconv4/alphasconv4/biasesconv4/weights
fc1/biasesfc1/weightslandmark_fc/biaseslandmark_fc/weights*"
dtypes
2
e
save/control_dependencyIdentity
save/Const^save/SaveV2*
T0*
_class
loc:@save/Const
?
save/RestoreV2/tensor_namesConst"/device:CPU:0*?
value?B?Bbbox_fc/biasesBbbox_fc/weightsBcls_fc/biasesBcls_fc/weightsBconv1/alphasBconv1/biasesBconv1/weightsBconv2/alphasBconv2/biasesBconv2/weightsBconv3/alphasBconv3/biasesBconv3/weightsBconv4/alphasBconv4/biasesBconv4/weightsB
fc1/biasesBfc1/weightsBlandmark_fc/biasesBlandmark_fc/weights*
dtype0
?
save/RestoreV2/shape_and_slicesConst"/device:CPU:0*;
value2B0B B B B B B B B B B B B B B B B B B B B *
dtype0
?
save/RestoreV2	RestoreV2
save/Constsave/RestoreV2/tensor_namessave/RestoreV2/shape_and_slices"/device:CPU:0*"
dtypes
2
?
save/AssignAssignbbox_fc/biasessave/RestoreV2*
T0*
use_locking(*
validate_shape(*!
_class
loc:@bbox_fc/biases
?
save/Assign_1Assignbbox_fc/weightssave/RestoreV2:1*
T0*
use_locking(*
validate_shape(*"
_class
loc:@bbox_fc/weights
?
save/Assign_2Assigncls_fc/biasessave/RestoreV2:2*
T0*
use_locking(*
validate_shape(* 
_class
loc:@cls_fc/biases
?
save/Assign_3Assigncls_fc/weightssave/RestoreV2:3*
T0*
use_locking(*
validate_shape(*!
_class
loc:@cls_fc/weights
?
save/Assign_4Assignconv1/alphassave/RestoreV2:4*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv1/alphas
?
save/Assign_5Assignconv1/biasessave/RestoreV2:5*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv1/biases
?
save/Assign_6Assignconv1/weightssave/RestoreV2:6*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv1/weights
?
save/Assign_7Assignconv2/alphassave/RestoreV2:7*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv2/alphas
?
save/Assign_8Assignconv2/biasessave/RestoreV2:8*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv2/biases
?
save/Assign_9Assignconv2/weightssave/RestoreV2:9*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv2/weights
?
save/Assign_10Assignconv3/alphassave/RestoreV2:10*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv3/alphas
?
save/Assign_11Assignconv3/biasessave/RestoreV2:11*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv3/biases
?
save/Assign_12Assignconv3/weightssave/RestoreV2:12*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv3/weights
?
save/Assign_13Assignconv4/alphassave/RestoreV2:13*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv4/alphas
?
save/Assign_14Assignconv4/biasessave/RestoreV2:14*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv4/biases
?
save/Assign_15Assignconv4/weightssave/RestoreV2:15*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv4/weights
?
save/Assign_16Assign
fc1/biasessave/RestoreV2:16*
T0*
use_locking(*
validate_shape(*
_class
loc:@fc1/biases
?
save/Assign_17Assignfc1/weightssave/RestoreV2:17*
T0*
use_locking(*
validate_shape(*
_class
loc:@fc1/weights
?
save/Assign_18Assignlandmark_fc/biasessave/RestoreV2:18*
T0*
use_locking(*
validate_shape(*%
_class
loc:@landmark_fc/biases
?
save/Assign_19Assignlandmark_fc/weightssave/RestoreV2:19*
T0*
use_locking(*
validate_shape(*&
_class
loc:@landmark_fc/weights
?
save/restore_allNoOp^save/Assign^save/Assign_1^save/Assign_10^save/Assign_11^save/Assign_12^save/Assign_13^save/Assign_14^save/Assign_15^save/Assign_16^save/Assign_17^save/Assign_18^save/Assign_19^save/Assign_2^save/Assign_3^save/Assign_4^save/Assign_5^save/Assign_6^save/Assign_7^save/Assign_8^save/Assign_9"