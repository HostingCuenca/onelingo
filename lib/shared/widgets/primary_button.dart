import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

import '../../app/theme.dart';

/// Solid pedestal and a small press movement, including keyboard activation.
class BotonPrincipal extends StatefulWidget {
  const BotonPrincipal({
    super.key,
    required this.onPressed,
    required this.child,
    this.color = OL.morado,
  });
  final VoidCallback? onPressed;
  final Widget child;
  final Color color;
  @override
  State<BotonPrincipal> createState() => _BotonPrincipalState();
}

class _BotonPrincipalState extends State<BotonPrincipal> {
  final states = WidgetStatesController();
  @override
  void initState() {
    super.initState();
    states.addListener(_update);
  }

  void _update() {
    if (SchedulerBinding.instance.schedulerPhase ==
        SchedulerPhase.persistentCallbacks) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) setState(() {});
      });
    } else if (mounted) {
      setState(() {});
    }
  }

  @override
  void dispose() {
    states.removeListener(_update);
    states.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final pressed = states.value.contains(WidgetState.pressed);
    final enabled = widget.onPressed != null;
    return Padding(
      padding: const EdgeInsets.only(bottom: 5, top: 8),
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: enabled
              ? Color.lerp(widget.color, OL.texto, .25)!
              : OL.grisClaro,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Padding(
          padding: const EdgeInsets.only(bottom: 4),
          child: AnimatedSlide(
            duration: MediaQuery.disableAnimationsOf(context)
                ? Duration.zero
                : const Duration(milliseconds: 90),
            offset: Offset(0, pressed && enabled ? .065 : 0),
            child: ElevatedButton(
              statesController: states,
              onPressed: widget.onPressed,
              style: ElevatedButton.styleFrom(
                backgroundColor: widget.color,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                padding: const EdgeInsets.symmetric(
                  horizontal: 18,
                  vertical: 16,
                ),
              ),
              child: widget.child,
            ),
          ),
        ),
      ),
    );
  }
}
