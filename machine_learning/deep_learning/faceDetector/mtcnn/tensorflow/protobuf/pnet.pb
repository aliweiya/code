
6
input_imagePlaceholder*
dtype0*
shape:
6
image_widthPlaceholder*
dtype0*
shape:
7
image_heightPlaceholder*
dtype0*
shape:
9
Reshape/shape/0Const*
value	B :*
dtype0
9
Reshape/shape/3Const*
value	B :*
dtype0
p
Reshape/shapePackReshape/shape/0image_heightimage_widthReshape/shape/3*

axis *
T0*
N
E
ReshapeReshapeinput_imageReshape/shape*
T0*
Tshape0
?
.conv1/weights/Initializer/random_uniform/shapeConst*%
valueB"         
   *
dtype0* 
_class
loc:@conv1/weights
{
,conv1/weights/Initializer/random_uniform/minConst*
valueB
 *??g?*
dtype0* 
_class
loc:@conv1/weights
{
,conv1/weights/Initializer/random_uniform/maxConst*
valueB
 *??g>*
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
shape:
* 
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
valueB
*    *
dtype0*
_class
loc:@conv1/biases
}
conv1/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:
*
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
conv1/Conv2DConv2DReshapeconv1/weights/read*
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
valueB
*  ?>*
dtype0*
_class
loc:@conv1/alphas
}
conv1/alphas
VariableV2*
dtype0*
shared_name *
	container *
shape:
*
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

?
.conv2/weights/Initializer/random_uniform/shapeConst*%
valueB"      
      *
dtype0* 
_class
loc:@conv2/weights
{
,conv2/weights/Initializer/random_uniform/minConst*
valueB
 *??#?*
dtype0* 
_class
loc:@conv2/weights
{
,conv2/weights/Initializer/random_uniform/maxConst*
valueB
 *??#>*
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
shape:
* 
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
valueB*    *
dtype0*
_class
loc:@conv2/biases
}
conv2/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:*
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
valueB*  ?>*
dtype0*
_class
loc:@conv2/alphas
}
conv2/alphas
VariableV2*
dtype0*
shared_name *
	container *
shape:*
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
?
.conv3/weights/Initializer/random_uniform/shapeConst*%
valueB"             *
dtype0* 
_class
loc:@conv3/weights
{
,conv3/weights/Initializer/random_uniform/minConst*
valueB
 *?[??*
dtype0* 
_class
loc:@conv3/weights
{
,conv3/weights/Initializer/random_uniform/maxConst*
valueB
 *?[?=*
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
shape: * 
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
valueB *    *
dtype0*
_class
loc:@conv3/biases
}
conv3/biases
VariableV2*
dtype0*
shared_name *
	container *
shape: *
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
conv3/Conv2DConv2D	conv2/addconv3/weights/read*
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
valueB *  ?>*
dtype0*
_class
loc:@conv3/alphas
}
conv3/alphas
VariableV2*
dtype0*
shared_name *
	container *
shape: *
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
?
0conv4_1/weights/Initializer/random_uniform/shapeConst*%
valueB"             *
dtype0*"
_class
loc:@conv4_1/weights

.conv4_1/weights/Initializer/random_uniform/minConst*
valueB
 *A׾*
dtype0*"
_class
loc:@conv4_1/weights

.conv4_1/weights/Initializer/random_uniform/maxConst*
valueB
 *A?>*
dtype0*"
_class
loc:@conv4_1/weights
?
8conv4_1/weights/Initializer/random_uniform/RandomUniformRandomUniform0conv4_1/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed *"
_class
loc:@conv4_1/weights
?
.conv4_1/weights/Initializer/random_uniform/subSub.conv4_1/weights/Initializer/random_uniform/max.conv4_1/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@conv4_1/weights
?
.conv4_1/weights/Initializer/random_uniform/mulMul8conv4_1/weights/Initializer/random_uniform/RandomUniform.conv4_1/weights/Initializer/random_uniform/sub*
T0*"
_class
loc:@conv4_1/weights
?
*conv4_1/weights/Initializer/random_uniformAdd.conv4_1/weights/Initializer/random_uniform/mul.conv4_1/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@conv4_1/weights
?
conv4_1/weights
VariableV2*
dtype0*
shared_name *
	container *
shape: *"
_class
loc:@conv4_1/weights
?
conv4_1/weights/AssignAssignconv4_1/weights*conv4_1/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(*"
_class
loc:@conv4_1/weights
^
conv4_1/weights/readIdentityconv4_1/weights*
T0*"
_class
loc:@conv4_1/weights
?
/conv4_1/kernel/Regularizer/l2_regularizer/scaleConst*
valueB
 *o:*
dtype0*"
_class
loc:@conv4_1/weights
}
0conv4_1/kernel/Regularizer/l2_regularizer/L2LossL2Lossconv4_1/weights/read*
T0*"
_class
loc:@conv4_1/weights
?
)conv4_1/kernel/Regularizer/l2_regularizerMul/conv4_1/kernel/Regularizer/l2_regularizer/scale0conv4_1/kernel/Regularizer/l2_regularizer/L2Loss*
T0*"
_class
loc:@conv4_1/weights
t
 conv4_1/biases/Initializer/zerosConst*
valueB*    *
dtype0*!
_class
loc:@conv4_1/biases
?
conv4_1/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:*!
_class
loc:@conv4_1/biases
?
conv4_1/biases/AssignAssignconv4_1/biases conv4_1/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*!
_class
loc:@conv4_1/biases
[
conv4_1/biases/readIdentityconv4_1/biases*
T0*!
_class
loc:@conv4_1/biases
J
conv4_1/dilation_rateConst*
valueB"      *
dtype0
?
conv4_1/Conv2DConv2D	conv3/addconv4_1/weights/read*
strides
*
	dilations
*
T0*
data_formatNHWC*
paddingVALID*
use_cudnn_on_gpu(
_
conv4_1/BiasAddBiasAddconv4_1/Conv2Dconv4_1/biases/read*
T0*
data_formatNHWC
4
conv4_1/SoftmaxSoftmaxconv4_1/BiasAdd*
T0
?
0conv4_2/weights/Initializer/random_uniform/shapeConst*%
valueB"             *
dtype0*"
_class
loc:@conv4_2/weights

.conv4_2/weights/Initializer/random_uniform/minConst*
valueB
 *?Ѿ*
dtype0*"
_class
loc:@conv4_2/weights

.conv4_2/weights/Initializer/random_uniform/maxConst*
valueB
 *??>*
dtype0*"
_class
loc:@conv4_2/weights
?
8conv4_2/weights/Initializer/random_uniform/RandomUniformRandomUniform0conv4_2/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed *"
_class
loc:@conv4_2/weights
?
.conv4_2/weights/Initializer/random_uniform/subSub.conv4_2/weights/Initializer/random_uniform/max.conv4_2/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@conv4_2/weights
?
.conv4_2/weights/Initializer/random_uniform/mulMul8conv4_2/weights/Initializer/random_uniform/RandomUniform.conv4_2/weights/Initializer/random_uniform/sub*
T0*"
_class
loc:@conv4_2/weights
?
*conv4_2/weights/Initializer/random_uniformAdd.conv4_2/weights/Initializer/random_uniform/mul.conv4_2/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@conv4_2/weights
?
conv4_2/weights
VariableV2*
dtype0*
shared_name *
	container *
shape: *"
_class
loc:@conv4_2/weights
?
conv4_2/weights/AssignAssignconv4_2/weights*conv4_2/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(*"
_class
loc:@conv4_2/weights
^
conv4_2/weights/readIdentityconv4_2/weights*
T0*"
_class
loc:@conv4_2/weights
?
/conv4_2/kernel/Regularizer/l2_regularizer/scaleConst*
valueB
 *o:*
dtype0*"
_class
loc:@conv4_2/weights
}
0conv4_2/kernel/Regularizer/l2_regularizer/L2LossL2Lossconv4_2/weights/read*
T0*"
_class
loc:@conv4_2/weights
?
)conv4_2/kernel/Regularizer/l2_regularizerMul/conv4_2/kernel/Regularizer/l2_regularizer/scale0conv4_2/kernel/Regularizer/l2_regularizer/L2Loss*
T0*"
_class
loc:@conv4_2/weights
t
 conv4_2/biases/Initializer/zerosConst*
valueB*    *
dtype0*!
_class
loc:@conv4_2/biases
?
conv4_2/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:*!
_class
loc:@conv4_2/biases
?
conv4_2/biases/AssignAssignconv4_2/biases conv4_2/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*!
_class
loc:@conv4_2/biases
[
conv4_2/biases/readIdentityconv4_2/biases*
T0*!
_class
loc:@conv4_2/biases
J
conv4_2/dilation_rateConst*
valueB"      *
dtype0
?
conv4_2/Conv2DConv2D	conv3/addconv4_2/weights/read*
strides
*
	dilations
*
T0*
data_formatNHWC*
paddingVALID*
use_cudnn_on_gpu(
_
conv4_2/BiasAddBiasAddconv4_2/Conv2Dconv4_2/biases/read*
T0*
data_formatNHWC
?
0conv4_3/weights/Initializer/random_uniform/shapeConst*%
valueB"          
   *
dtype0*"
_class
loc:@conv4_3/weights

.conv4_3/weights/Initializer/random_uniform/minConst*
valueB
 *????*
dtype0*"
_class
loc:@conv4_3/weights

.conv4_3/weights/Initializer/random_uniform/maxConst*
valueB
 *???>*
dtype0*"
_class
loc:@conv4_3/weights
?
8conv4_3/weights/Initializer/random_uniform/RandomUniformRandomUniform0conv4_3/weights/Initializer/random_uniform/shape*
T0*
dtype0*
seed2 *

seed *"
_class
loc:@conv4_3/weights
?
.conv4_3/weights/Initializer/random_uniform/subSub.conv4_3/weights/Initializer/random_uniform/max.conv4_3/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@conv4_3/weights
?
.conv4_3/weights/Initializer/random_uniform/mulMul8conv4_3/weights/Initializer/random_uniform/RandomUniform.conv4_3/weights/Initializer/random_uniform/sub*
T0*"
_class
loc:@conv4_3/weights
?
*conv4_3/weights/Initializer/random_uniformAdd.conv4_3/weights/Initializer/random_uniform/mul.conv4_3/weights/Initializer/random_uniform/min*
T0*"
_class
loc:@conv4_3/weights
?
conv4_3/weights
VariableV2*
dtype0*
shared_name *
	container *
shape: 
*"
_class
loc:@conv4_3/weights
?
conv4_3/weights/AssignAssignconv4_3/weights*conv4_3/weights/Initializer/random_uniform*
T0*
use_locking(*
validate_shape(*"
_class
loc:@conv4_3/weights
^
conv4_3/weights/readIdentityconv4_3/weights*
T0*"
_class
loc:@conv4_3/weights
?
/conv4_3/kernel/Regularizer/l2_regularizer/scaleConst*
valueB
 *o:*
dtype0*"
_class
loc:@conv4_3/weights
}
0conv4_3/kernel/Regularizer/l2_regularizer/L2LossL2Lossconv4_3/weights/read*
T0*"
_class
loc:@conv4_3/weights
?
)conv4_3/kernel/Regularizer/l2_regularizerMul/conv4_3/kernel/Regularizer/l2_regularizer/scale0conv4_3/kernel/Regularizer/l2_regularizer/L2Loss*
T0*"
_class
loc:@conv4_3/weights
t
 conv4_3/biases/Initializer/zerosConst*
valueB
*    *
dtype0*!
_class
loc:@conv4_3/biases
?
conv4_3/biases
VariableV2*
dtype0*
shared_name *
	container *
shape:
*!
_class
loc:@conv4_3/biases
?
conv4_3/biases/AssignAssignconv4_3/biases conv4_3/biases/Initializer/zeros*
T0*
use_locking(*
validate_shape(*!
_class
loc:@conv4_3/biases
[
conv4_3/biases/readIdentityconv4_3/biases*
T0*!
_class
loc:@conv4_3/biases
J
conv4_3/dilation_rateConst*
valueB"      *
dtype0
?
conv4_3/Conv2DConv2D	conv3/addconv4_3/weights/read*
strides
*
	dilations
*
T0*
data_formatNHWC*
paddingVALID*
use_cudnn_on_gpu(
_
conv4_3/BiasAddBiasAddconv4_3/Conv2Dconv4_3/biases/read*
T0*
data_formatNHWC
8

save/ConstConst*
valueB Bmodel*
dtype0
?
save/SaveV2/tensor_namesConst*?
value?B?Bconv1/alphasBconv1/biasesBconv1/weightsBconv2/alphasBconv2/biasesBconv2/weightsBconv3/alphasBconv3/biasesBconv3/weightsBconv4_1/biasesBconv4_1/weightsBconv4_2/biasesBconv4_2/weightsBconv4_3/biasesBconv4_3/weights*
dtype0
e
save/SaveV2/shape_and_slicesConst*1
value(B&B B B B B B B B B B B B B B B *
dtype0
?
save/SaveV2SaveV2
save/Constsave/SaveV2/tensor_namessave/SaveV2/shape_and_slicesconv1/alphasconv1/biasesconv1/weightsconv2/alphasconv2/biasesconv2/weightsconv3/alphasconv3/biasesconv3/weightsconv4_1/biasesconv4_1/weightsconv4_2/biasesconv4_2/weightsconv4_3/biasesconv4_3/weights*
dtypes
2
e
save/control_dependencyIdentity
save/Const^save/SaveV2*
T0*
_class
loc:@save/Const
?
save/RestoreV2/tensor_namesConst"/device:CPU:0*?
value?B?Bconv1/alphasBconv1/biasesBconv1/weightsBconv2/alphasBconv2/biasesBconv2/weightsBconv3/alphasBconv3/biasesBconv3/weightsBconv4_1/biasesBconv4_1/weightsBconv4_2/biasesBconv4_2/weightsBconv4_3/biasesBconv4_3/weights*
dtype0
w
save/RestoreV2/shape_and_slicesConst"/device:CPU:0*1
value(B&B B B B B B B B B B B B B B B *
dtype0
?
save/RestoreV2	RestoreV2
save/Constsave/RestoreV2/tensor_namessave/RestoreV2/shape_and_slices"/device:CPU:0*
dtypes
2
?
save/AssignAssignconv1/alphassave/RestoreV2*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv1/alphas
?
save/Assign_1Assignconv1/biasessave/RestoreV2:1*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv1/biases
?
save/Assign_2Assignconv1/weightssave/RestoreV2:2*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv1/weights
?
save/Assign_3Assignconv2/alphassave/RestoreV2:3*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv2/alphas
?
save/Assign_4Assignconv2/biasessave/RestoreV2:4*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv2/biases
?
save/Assign_5Assignconv2/weightssave/RestoreV2:5*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv2/weights
?
save/Assign_6Assignconv3/alphassave/RestoreV2:6*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv3/alphas
?
save/Assign_7Assignconv3/biasessave/RestoreV2:7*
T0*
use_locking(*
validate_shape(*
_class
loc:@conv3/biases
?
save/Assign_8Assignconv3/weightssave/RestoreV2:8*
T0*
use_locking(*
validate_shape(* 
_class
loc:@conv3/weights
?
save/Assign_9Assignconv4_1/biasessave/RestoreV2:9*
T0*
use_locking(*
validate_shape(*!
_class
loc:@conv4_1/biases
?
save/Assign_10Assignconv4_1/weightssave/RestoreV2:10*
T0*
use_locking(*
validate_shape(*"
_class
loc:@conv4_1/weights
?
save/Assign_11Assignconv4_2/biasessave/RestoreV2:11*
T0*
use_locking(*
validate_shape(*!
_class
loc:@conv4_2/biases
?
save/Assign_12Assignconv4_2/weightssave/RestoreV2:12*
T0*
use_locking(*
validate_shape(*"
_class
loc:@conv4_2/weights
?
save/Assign_13Assignconv4_3/biasessave/RestoreV2:13*
T0*
use_locking(*
validate_shape(*!
_class
loc:@conv4_3/biases
?
save/Assign_14Assignconv4_3/weightssave/RestoreV2:14*
T0*
use_locking(*
validate_shape(*"
_class
loc:@conv4_3/weights
?
save/restore_allNoOp^save/Assign^save/Assign_1^save/Assign_10^save/Assign_11^save/Assign_12^save/Assign_13^save/Assign_14^save/Assign_2^save/Assign_3^save/Assign_4^save/Assign_5^save/Assign_6^save/Assign_7^save/Assign_8^save/Assign_9"