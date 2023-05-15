
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as niu

from nipype.interfaces.niftyreg.regutils import RegResample

from macapype.nodes.prepare import padding_cropped_img


def pad_brain_extraction_pipe(seg_pipe, params, inputnode, outputnode,
                              data_preparation_pipe,
                              brain_extraction_pipe, ):

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():

            print("Padding mask in native space")

            pad_mask = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_mask")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.brain_mask",
                             pad_mask, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_mask, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_mask, "indiv_crop")

            seg_pipe.connect(pad_mask, "padded_img_file",
                             outputnode, "brain_mask")

            print("Padding debiased_T1 in native space")

            pad_debiased_T1 = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_debiased_T1")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.debiased_T1",
                             pad_debiased_T1, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_debiased_T1, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_debiased_T1, "indiv_crop")

            seg_pipe.connect(pad_debiased_T1, "padded_img_file",
                             outputnode, "debiased_T1")

        elif "bet_crop" in params["short_preparation_pipe"].keys():
            print("Not implemented yet")

        else:
            print("Using reg_aladin transfo to pad mask back")
            pad_mask = pe.Node(RegResample(inter_val="NN"),
                               name="pad_mask")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.brain_mask",
                             pad_mask, "flo_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_mask, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                             "inv_tranfo.out_file",
                             pad_mask, "trans_file")

            print("Using reg_aladin transfo to pad debiased_T1 back")
            pad_debiased_T1 = pe.Node(RegResample(),
                                      name="pad_debiased_T1")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.debiased_T1",
                             pad_debiased_T1, "flo_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_debiased_T1, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                             "inv_tranfo.out_file",
                             pad_debiased_T1, "trans_file")

            # outputnode
            seg_pipe.connect(pad_mask, "out_file",
                             outputnode, "brain_mask")

            seg_pipe.connect(pad_debiased_T1, "out_file",
                             outputnode, "debiased_T1")

    elif "long_single_preparation_pipe" in params.keys():
        if "prep_T1" in params["long_single_preparation_pipe"].keys():

            print("Padding mask in native space \
                (long_single_preparation_pipe)")

            pad_mask = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_mask")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.brain_mask",
                             pad_mask, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_mask, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_mask, "indiv_crop")

            seg_pipe.connect(pad_mask, "padded_img_file",
                             outputnode, "brain_mask")

            print("Padding debiased_T1 in native space")

            pad_debiased_T1 = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_debiased_T1")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.debiased_T1",
                             pad_debiased_T1, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_debiased_T1, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_debiased_T1, "indiv_crop")

            seg_pipe.connect(pad_debiased_T1, "padded_img_file",
                             outputnode, "debiased_T1")

def pad_brain_segment_pipe(seg_pipe, params,
                           inputnode, outputnode,
                           data_preparation_pipe,
                           brain_extraction_pipe, brain_segment_pipe,):

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():

            print("Padding seg_mask in native space")

            pad_seg_mask = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_seg_mask")

            seg_pipe.connect(brain_segment_pipe,
                             "outputnode.segmented_file",
                             pad_seg_mask, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_seg_mask, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_seg_mask, "indiv_crop")

            seg_pipe.connect(pad_seg_mask, "padded_img_file",
                             outputnode, "segmented_brain_mask")

        elif "bet_crop" in params["short_preparation_pipe"].keys():
            print("Not implemented yet")

        else:
            print("Using reg_aladin transfo to pad seg_mask back")

            pad_seg_mask = pe.Node(RegResample(inter_val="NN"),
                                   name="pad_seg_mask")

            seg_pipe.connect(brain_segment_pipe,
                             "outputnode.segmented_file",
                             pad_seg_mask, "flo_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_seg_mask, "ref_file")

            seg_pipe.connect(data_preparation_pipe, "inv_tranfo.out_file",
                             pad_seg_mask, "trans_file")

            # outputnode
            seg_pipe.connect(pad_seg_mask, "out_file",
                             outputnode, "segmented_brain_mask")

    elif "long_single_preparation_pipe" in params.keys():
        if "prep_T1" in params["long_single_preparation_pipe"].keys():

            print("Padding seg_mask in native space")

            pad_seg_mask = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_seg_mask")

            seg_pipe.connect(brain_segment_pipe,
                             "outputnode.segmented_file",
                             pad_seg_mask, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                             pad_seg_mask, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_seg_mask, "indiv_crop")

            seg_pipe.connect(pad_seg_mask, "padded_img_file",
                             outputnode, "segmented_brain_mask")

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():

            print("Padding debiased_brain in native space")

            pad_debiased_brain = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_debiased_brain")

            seg_pipe.connect(brain_segment_pipe,
                            "outputnode.debiased_brain",
                            pad_debiased_brain, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                            pad_debiased_brain, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                            pad_debiased_brain, "indiv_crop")

            seg_pipe.connect(pad_debiased_brain, "padded_img_file",
                            outputnode, "debiased_brain")

        elif "bet_crop" in params["short_preparation_pipe"].keys():
            print("Not implemented yet")

        else:
            print("Using reg_aladin transfo to pad debiased_brain back")

            pad_debiased_brain = pe.Node(RegResample(),
                                        name="pad_debiased_brain")

            seg_pipe.connect(brain_segment_pipe,
                            "outputnode.debiased_brain",
                            pad_debiased_brain, "flo_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                            pad_debiased_brain, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                            "inv_tranfo.out_file",
                            pad_debiased_brain, "trans_file")

            # outputnode
            seg_pipe.connect(pad_debiased_brain, "out_file",
                            outputnode, "debiased_brain")

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():

            print("Padding prob_csf in native space")

            pad_prob_csf = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                    'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_prob_csf")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_csf",
                                pad_prob_csf, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_csf, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                                pad_prob_csf, "indiv_crop")

            seg_pipe.connect(pad_prob_csf, "padded_img_file",
                                outputnode, "prob_csf")

        elif "bet_crop" in params["short_preparation_pipe"].keys():
            print("Not implemented yet")

        else:
            print("Using reg_aladin transfo to pad prob_csf back")

            pad_prob_csf = pe.Node(RegResample(),
                                    name="pad_prob_csf")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_csf",
                                pad_prob_csf, "flo_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_csf, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                                "inv_tranfo.out_file",
                                pad_prob_csf, "trans_file")

            # outputnode
            seg_pipe.connect(pad_prob_csf, "out_file",
                                outputnode, "prob_csf")

    elif "long_single_preparation_pipe" in params.keys():
        if "prep_T1" in params["long_single_preparation_pipe"].keys():

            print("Padding prob_csf in native space")

            pad_prob_csf = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                    'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_prob_csf")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_csf",
                                pad_prob_csf, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_csf, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                                pad_prob_csf, "indiv_crop")

            seg_pipe.connect(pad_prob_csf, "padded_img_file",
                                outputnode, "prob_csf")

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():

            print("Padding prob_gm in native space")

            pad_prob_gm = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                    'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_prob_gm")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_gm",
                                pad_prob_gm, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_gm, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                                pad_prob_gm, "indiv_crop")

            seg_pipe.connect(pad_prob_gm, "padded_img_file",
                                outputnode, "prob_gm")

        elif "bet_crop" in params["short_preparation_pipe"].keys():
            print("Not implemented yet")

        else:
            print("Using reg_aladin transfo to pad prob_gm back")

            pad_prob_gm = pe.Node(RegResample(),
                                    name="pad_prob_gm")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_gm",
                                pad_prob_gm, "flo_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_gm, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                                "inv_tranfo.out_file",
                                pad_prob_gm, "trans_file")

            # outputnode
            seg_pipe.connect(pad_prob_gm, "out_file",
                                outputnode, "prob_gm")

    elif "long_single_preparation_pipe" in params.keys():
        if "prep_T1" in params["long_single_preparation_pipe"].keys():

            print("Padding prob_gm in native space")

            pad_prob_gm = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                    'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_prob_gm")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_gm",
                                pad_prob_gm, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_gm, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                                pad_prob_gm, "indiv_crop")

            seg_pipe.connect(pad_prob_gm, "padded_img_file",
                                outputnode, "prob_gm")

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():

            print("Padding prob_wm in native space")

            pad_prob_wm = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                    'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_prob_wm")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_wm",
                                pad_prob_wm, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_wm, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                                pad_prob_wm, "indiv_crop")

            seg_pipe.connect(pad_prob_wm, "padded_img_file",
                                outputnode, "prob_wm")

        elif "bet_crop" in params["short_preparation_pipe"].keys():
            print("Not implemented yet")

        else:
            print("Using reg_aladin transfo to pad prob_wm back")

            pad_prob_wm = pe.Node(RegResample(),
                                    name="pad_prob_wm")

            seg_pipe.connect(brain_segment_pipe, "outputnode.prob_wm",
                                pad_prob_wm, "flo_file")

            seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                pad_prob_wm, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                                "inv_tranfo.out_file",
                                pad_prob_wm, "trans_file")

            # outputnode
            seg_pipe.connect(pad_prob_wm, "out_file",
                                outputnode, "prob_wm")

        if "export_5tt_pipe" in params["brain_segment_pipe"]:

            if "short_preparation_pipe" in params.keys():
                if "crop_T1" in params["short_preparation_pipe"].keys():

                    print("Padding gen_5tt in native space")

                    pad_gen_5tt = pe.Node(
                        niu.Function(
                            input_names=['cropped_img_file', 'orig_img_file',
                                         'indiv_crop'],
                            output_names=['padded_img_file'],
                            function=padding_cropped_img),
                        name="pad_gen_5tt")

                    seg_pipe.connect(brain_segment_pipe, "outputnode.gen_5tt",
                                     pad_gen_5tt, "cropped_img_file")

                    seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                     pad_gen_5tt, "orig_img_file")

                    seg_pipe.connect(inputnode, "indiv_params",
                                     pad_gen_5tt, "indiv_crop")

                    seg_pipe.connect(pad_gen_5tt, "padded_img_file",
                                     outputnode, "gen_5tt")

                elif "bet_crop" in params["short_preparation_pipe"].keys():
                    print("Not implemented yet")

                else:
                    print("Using reg_aladin transfo to pad gen_5tt back")

                    pad_gen_5tt = pe.Node(RegResample(inter_val='NN'),
                                          name="pad_gen_5tt")

                    seg_pipe.connect(brain_segment_pipe, "outputnode.gen_5tt",
                                     pad_gen_5tt, "flo_file")

                    seg_pipe.connect(data_preparation_pipe, "av_T1.avg_img",
                                     pad_gen_5tt, "ref_file")

                    seg_pipe.connect(data_preparation_pipe,
                                     "inv_tranfo.out_file",
                                     pad_gen_5tt, "trans_file")

                    # outputnode
                    seg_pipe.connect(pad_gen_5tt, "out_file",
                                     outputnode, "gen_5tt")


def pad_native_to_stereo_pipe(seg_pipe, params, inputnode, outputnode,
                              data_preparation_pipe, native_to_stereo_pipe):

        if "brain_extraction_pipe" in params.keys() and pad:

            # apply transfo to list
            stereo_mask = pe.Node(RegResample(inter_val="NN"),
                                  name='stereo_mask')

            seg_pipe.connect(pad_mask, 'out_file',
                             stereo_mask, "flo_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.transfo_native_to_stereo',
                             stereo_mask, "trans_file")

            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.padded_stereo_T1',
                             stereo_mask, "ref_file")

            seg_pipe.connect(stereo_mask, "out_file",
                             outputnode, "stereo_brain_mask")

            # apply transfo to list
            stereo_debiased_T1 = pe.Node(RegResample(inter_val="NN"),
                                  name='stereo_debiased_T1')

            seg_pipe.connect(pad_debiased_T1, 'out_file',
                             stereo_debiased_T1, "flo_file")

            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.transfo_native_to_stereo',
                             stereo_debiased_T1, "trans_file")

            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.padded_stereo_T1',
                             stereo_debiased_T1, "ref_file")

            seg_pipe.connect(stereo_debiased_T1, "out_file",
                             outputnode, "stereo_brain_debiased_T1")

        if "brain_segment_pipe" in params.keys() and pad:

            # apply transfo to list
            stereo_prob_gm = pe.Node(RegResample(inter_val="LIN"),
                                  name='stereo_prob_gm')

            seg_pipe.connect(pad_prob_gm, 'out_file',
                             stereo_prob_gm, "flo_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.transfo_native_to_stereo',
                             stereo_prob_gm, "trans_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.padded_stereo_T1',
                             stereo_prob_gm, "ref_file")

            seg_pipe.connect(stereo_prob_gm, "out_file",
                             outputnode, "stereo_prob_gm")

            # apply transfo to list
            stereo_prob_wm = pe.Node(RegResample(inter_val="LIN"),
                                  name='stereo_prob_wm')

            seg_pipe.connect(pad_prob_wm, 'out_file',
                             stereo_prob_wm, "flo_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.transfo_native_to_stereo',
                             stereo_prob_wm, "trans_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.padded_stereo_T1',
                             stereo_prob_wm, "ref_file")

            seg_pipe.connect(stereo_prob_wm, "out_file",
                             outputnode, "stereo_prob_wm")

            # apply transfo to list
            stereo_prob_csf = pe.Node(RegResample(inter_val="LIN"),
                                      name='stereo_prob_csf')

            seg_pipe.connect(pad_prob_csf, 'out_file',
                             stereo_prob_csf, "flo_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.transfo_native_to_stereo',
                             stereo_prob_csf, "trans_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.padded_stereo_T1',
                             stereo_prob_csf, "ref_file")

            seg_pipe.connect(stereo_prob_csf, "out_file",
                             outputnode, "stereo_prob_csf")

            # apply transfo to list
            stereo_seg_mask = pe.Node(RegResample(inter_val="NN"),
                                      name='stereo_seg_mask')

            seg_pipe.connect(pad_seg_mask, 'out_file',
                             stereo_seg_mask, "flo_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.transfo_native_to_stereo',
                             stereo_seg_mask, "trans_file")
            seg_pipe.connect(native_to_stereo_pipe,
                             'outputnode.padded_stereo_T1',
                             stereo_seg_mask, "ref_file")

            seg_pipe.connect(stereo_seg_mask, "out_file",
                             outputnode, "stereo_segmented_brain_mask")

            'stereo_segmented_brain_mask',
            "stereo_wmgm_mask"

            if "nii2mesh_brain_pipe" in params["brain_segment_pipe"]:

                # apply transfo to list
                stereo_wmgm_mask = pe.Node(RegResample(inter_val="NN"),
                                           name='stereo_wmgm_mask')

                seg_pipe.connect(nii2mesh_brain_pipe,
                                 "outputnode.wmgm_nii",
                                 stereo_wmgm_mask, "flo_file")

                seg_pipe.connect(native_to_stereo_pipe,
                                 'outputnode.transfo_native_to_stereo',
                                 stereo_wmgm_mask, "trans_file")

                seg_pipe.connect(native_to_stereo_pipe,
                                 'outputnode.padded_stereo_T1',
                                 stereo_wmgm_mask, "ref_file")

                seg_pipe.connect(stereo_wmgm_mask, "out_file",
                                 outputnode, "stereo_wmgm_mask")
